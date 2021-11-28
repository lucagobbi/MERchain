from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import notifications
from .models import *
from .forms import BidForm, ProductForm
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from .serializers import ProductSerializer
from notifications.signals import notify
from django.views.generic import ListView, View
from django.contrib.messages.views import SuccessMessageMixin
from notifications.models import Notification
import redis


r = redis.StrictRedis(host='127.0.0.1', port=6379, password='', db=0)

now = timezone.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

notifications = Notification.objects.all()


def home_view(request):
    products = Product.objects.exclude(done=True).order_by('-date_added')
    slider1 = products[:3]
    slider2 = products[3:6]


    for product in products:

        if product.deadline < now:

            if product.winner is None:
                product.done = True
                product.save()
                r.rpush(f'{product.name} - {product.user}', 'No winner for this auction')

                notify.send(request.user, recipient=request.user, verb=f'Your auction - {product.name} - is ended up without winners!', timestamp=now)


            else:
                product.done = True
                serializer = ProductSerializer(product)
                #product.writeOnChain(serializer)
                product.save()
                r.rpush(f'{product.name} - {product.user}', f'{product.winner} has won the auction')
                notify.send(product, recipient=product.user, verb=f'Congratulations your auction - {product.name} - is over: {product.winner} has won!', timestamp=now)
                notify.send(product, recipient=product.winner, verb=f'Congratulations you have won the {product.name} auction!', timestamp=now)



    context = {"products": products, "slider1": slider1, "slider2": slider2, "notifications": notifications}

    return render(request, 'store/homepage.html', context)


class StoreListView(ListView):
    paginate_by = 3
    context_object_name = 'products'
    template_name = "store/store.html"

    def get_queryset(self):
        return Product.objects.exclude(done=True).order_by('-date_added')
    


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    form = BidForm(request.POST)

    if request.method == "POST":
        bid = request.POST.get('amount')

        if form.is_valid():
            form.save(commit=False)

            if not product.user == user:

                if product.lastBid == 0:

                    if float(bid) > product.price:

                        product.lastBid = bid
                        product.winner = user
                        product.save()

                        r.rpush(f"{product.name} - {product.user}", f"{date_time} - {product.winner} bids {product.lastBid}$")

                        messages.success(request, 'Your bid has been recorded!')
                        notify.send(request.user, recipient=product.user, verb=f'{request.user.username} has bid {bid}$ on your product: {product.name}', timestamp=now)
                    
                    else: 
                        messages.warning(request, 'You have to bid an higher amount than the opening bid!')
                
                else:
                    if float(bid) > product.lastBid:

                        product.lastBid = bid
                        product.winner = user
                        product.save()

                        r.rpush(f"{product.name} - {product.user}", f"{date_time} - {product.winner} bids {product.lastBid}$")

                        messages.success(request, 'Your bid has been recorded!')
                        notify.send(request.user, recipient=product.user, verb=f'{request.user.username} has bid {bid}$ on your product: {product.name}', timestamp=now)


                
                    else:
                        messages.warning(request, 'You have to bid an higher amount than the last bid recorded!')

            else:
                messages.warning(request, 'You cannot bid on your own products!')
                    
    
    else:
        form = BidForm()


    context = {
        'product': product,
        'form': form,
        'notifications': notifications,
    }

    return render(request, 'store/product.html', context)



def new_product_view(request):

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=False)
            form.instance.user = request.user

            if form.instance.price < 0:
                messages.warning(request, 'You cannot place an order with a negative price!')
                return redirect('/newproduct/')

            if form.instance.deadline < now:
                messages.warning(request, 'You cannot set a deadline already reached!')
                return redirect('/newproduct/')

            form.save()
            notify.send(request.user, recipient=request.user, verb='Your Auction is Opened!', timestamp=now)
            return redirect('/')


    else:
        form = ProductForm()

    context = {
        'form': form,
        'notifications': notifications,
    }

    return render(request, 'store/newproduct.html', context)
 

def recap_view(request, pk):

   auction = get_object_or_404(Product, pk=pk)

   context = {
   'auction': auction,
   'notifications': notifications,
   }

   return render(request, 'store/recap.html', context)

def json_recap_view(request, pk):
    auction = get_object_or_404(Product, pk=pk)

    json = ProductSerializer(auction)
    
    return JsonResponse(json.data)

def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

    notifications.mark_all_as_read()
    notifications.update()

    context = {'notifications': notifications}

    return render(request, 'store/notifications.html', context)

def notifications_delete_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    notifications.delete()
    return redirect('/notifications/')

def search_view(request):

    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:
            return redirect("/search/")
        products = Product.objects.exclude(done=True).filter(name__icontains=querystring)
        context = {'products': products, 'querystring': querystring, 'notifications': notifications}
        return render(request, 'store/search.html', context) 

    else:
        return render(request, 'store/search.html')  


def about_view(request):
    context = {
        'notifications': notifications,
    }

    return render(request, 'store/about.html', context)



    




    



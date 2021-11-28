from store.models import Product
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import Profile
from django.utils import timezone
import notifications
from notifications.signals import notify
from notifications.models import Notification

now = timezone.now()

notifications = Notification.objects.all()

# view for the registration of a new user
def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            Profile.objects.create(user=user)
            login(request, user)
            notify.send(request.user, recipient=request.user, verb=f'Welcome to MERchain {user.username}!', timestamp=now)
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/registration.html", context)

def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    profile = Profile.objects.filter(user=user)
    products = Product.objects.exclude(done=True).filter(user=user)
    done = Product.objects.exclude(done=False).filter(user=user)
    won = Product.objects.exclude(done=False).filter(winner=user)

    
    context = {
        'user': user,
        'products': products,
        'profile': profile,
        'done': done,
        'won': won,
        'notifications': notifications,
    }

    return render(request, 'accounts/profile.html', context)
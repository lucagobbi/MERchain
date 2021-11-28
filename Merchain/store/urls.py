from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home_view, name='homepage'),
    path('store', v.StoreListView.as_view(), name='store'),
    path('product/<int:pk>/', v.product_view, name='product'),
    path('newproduct/', v.new_product_view, name='newproduct'),
    path('recap/<int:pk>/', v.recap_view, name='recap'),
    path('JSONrecap/<int:pk>/', v.json_recap_view, name='json_recap'),
    path('notifications/', v.notifications_view, name='view_all'),
    path('notifications/delete/', v.notifications_delete_view, name='delete'),
    path('search/', v.search_view, name="search"),
    path('about/', v.about_view, name='about'),
]
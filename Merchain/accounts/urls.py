from django.urls import path
from . import views as v
   
urlpatterns = [
    path('registration/', v.registration_view, name='registration'),
    path('profile/<int:id>/', v.profile_view, name='profile'),
] 

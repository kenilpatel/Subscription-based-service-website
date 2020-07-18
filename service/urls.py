from django.contrib import admin
from django.urls import path, reverse
from .views import Home, Login, Logout
from django_registration.backends.one_step.views import RegistrationView
urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path(
        'register/home/', Home.as_view(),
        name='home'
        ),
    path(
        'register/',
        RegistrationView.as_view(success_url='home/?message=done'),
        name='registeration'
        ),
    path(
        'login/',
        Login.as_view(),
        name='login'
        ),
    path(
        'logout/',
        Logout.as_view(),
        name='logout'
        ),
]

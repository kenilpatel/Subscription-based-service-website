from django.contrib import admin
from django.urls import path, reverse, re_path
from .views import Home, Login, Logout, Product,\
    CheckOut, User_service, Cancel, Restart
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
    re_path(
        r'.*login/',
        Login.as_view(),
        name='login'
    ),
    path(
        'logout/',
        Logout.as_view(),
        name='logout'
    ),
    path(
        'product/',
        Product.as_view(),
        name='product'
    ),
    path(
        'service/',
        User_service.as_view(),
        name='service'
    ),
    path(
        'checkout/',
        CheckOut.as_view(),
        name='checkout'
    ),
    re_path(
        r'.*cancel/',
        Cancel.as_view(),
        name='cancel'
    ),
    re_path(
        r'.*restart/',
        Restart.as_view(),
        name='restart'
    ),
]

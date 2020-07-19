from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import Service as srv, Subscriber
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
import stripe
import time
stripe.api_key = settings.STRIPE_API_KEY
# Create your views here.


class Home(TemplateView):
    template = "home.html"
    model = srv

    def get(self, request):
        data = self.model.objects.all()
        service = 0
        if("message" in request.GET.keys()):
            messages.add_message(
                request,
                messages.SUCCESS,
                'Registration done successfully'
            )
        for d in data:
            service = service + 1
        print(service)
        return render(request, self.template, {
            "total": service,
            "services": data
        })


class Login(TemplateView):
    template = "login.html"

    def get(self, request):
        return render(request, self.template, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.add_message(
                request,
                messages.SUCCESS,
                'Incorrect username or password')
        return render(request, self.template, {})


class Logout(TemplateView):

    def get(self, request):
        logout(request)
        return redirect("home")


class User_service(TemplateView):
    template = "service.html"

    @method_decorator(login_required(login_url="login/"))
    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})


class Product(TemplateView):
    template = "products.html"
    model = srv

    def get(self, request):
        data = self.model.objects.all()
        service = 0
        if("message" in request.GET.keys()):
            messages.add_message(
                request,
                messages.SUCCESS,
                'Registration done successfully'
            )
        for d in data:
            service = service + 1
        print(service)
        return render(request, self.template, {
            "total": service,
            "services": data
        })


class CheckOut(TemplateView):

    @method_decorator(login_required(login_url="login/"))
    def post(self, request):
        stripe_customer = stripe.Customer.create(
            email=request.user.email, source=request.POST['stripeToken'])
        plan = 'price_1H6O7TBfWC4lPABgcU5AD5CA'
        subscription = stripe.Subscription.create(customer=stripe_customer.id,
                                                  items=[{'plan': plan}],
                                                  trial_end=1595728813,)
        customer = Subscriber()
        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()
        return redirect("service")

    def get(self, request):
        return redirect("home")


class Cancel(TemplateView):
    @method_decorator(login_required(login_url="login/"))
    def get(self, request):
        print("cancel subscription")
        customer = Subscriber.objects.get(user=request.user)
        print(customer)
        if(customer):
            subscription = stripe.Subscription.retrieve(
                customer.stripe_subscription_id)
            subscription.cancel_at_period_end = True
            subscription.save()
            # ts = time.time()
            # trial_end = subscription.trial_end
            # if(ts > trial_end):
            #     print("trial is end")
            # else:
            #     print("currently in trial")
            return redirect("service")
        else:
            return redirect("service")


class Restart(TemplateView):
    @method_decorator(login_required(login_url="login/"))
    def get(self, request):
        print("restart subscription")
        customer = Subscriber.objects.get(user=request.user)
        if(customer):
            subscription = stripe.Subscription.retrieve(
                customer.stripe_subscription_id)
            if(subscription):
                subscription.cancel_at_period_end = False
                subscription.save()
                return redirect("service")
            else:
                return redirect("products")
        else:
            return redirect("products")
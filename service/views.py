from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import Service as srv, Subscription
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
import stripe
import time
from datetime import datetime, timedelta
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
        if(request.user.is_authenticated):
            return redirect("home")
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

    @method_decorator(login_required(login_url="login/"))
    def get(self, request):
        logout(request)
        return redirect("home")


class User_service(TemplateView):
    template = "service.html"
    model = srv

    @method_decorator(login_required(login_url="login/"))
    def get(self, request, *args, **kwargs):
        try:
            request.user.subscription
            subscription = stripe.Subscription.retrieve(
                request.user.subscription.stripe_subscription_id)
            request.user.subscription.state = subscription.status
            if(subscription.status == "canceled"):
                request.user.subscription.stripe_subscription_id = ""
                request.user.subscription.membership = False
                request.user.subscription.save()
            if(subscription.status == "active" or
                    subscription.status == "trialing"):
                request.user.subscription.membership = True
                request.user.subscription.save()
                t = int(time.time())
                trial = False
                days = 0
                if(subscription.status == "trialing"):
                    print("in if")
                    trial = True
                    days = int((subscription.trial_end - t) / 86400) + 1
                return render(request, self.template, {
                    'cancel': subscription.cancel_at_period_end,
                    'trial': trial,
                    'days': days})
            else:
                return redirect("product")
        except Subscription.DoesNotExist:
            return redirect("product")
        except stripe.error.InvalidRequestError:
            request.user.subscription.membership = False
            request.user.subscription.stripe_subscription_id = ""
            request.user.subscription.status = "not active"
            request.user.subscription.save()
            return redirect("product")


class Product(TemplateView):
    template = "products.html"
    model = srv

    def get(self, request):
        try:
            request.user.subscription
            subscription = stripe.Subscription.retrieve(
                request.user.subscription.stripe_subscription_id)
            request.user.subscription.state = subscription.status
            if(subscription.status == "canceled"):
                request.user.subscription.stripe_subscription_id = ""
                request.user.subscription.membership = False
                request.user.subscription.save()
            if(subscription.status == "active" or
                    subscription.status == "trialing"):
                request.user.subscription.membership = True
                request.user.subscription.save()
                return redirect("service")
            else:
                data = self.model.objects.all()
                service = 0
                for d in data:
                    service = service + 1
                print(service)
                return render(request, self.template, {
                    "total": service,
                    "services": data
                })
        except Subscription.DoesNotExist:
            data = self.model.objects.all()
            service = 0
            for d in data:
                service = service + 1
            print(service)
            return render(request, self.template, {
                "total": service,
                "services": data
            })
        except stripe.error.InvalidRequestError:
            data = self.model.objects.all()
            service = 0
            for d in data:
                service = service + 1
            request.user.subscription.stripe_subscription_id = ""
            request.user.subscription.membership = False
            request.user.subscription.status = "not active"
            request.user.subscription.save()
            return render(request, self.template, {
                "total": service,
                "services": data
            })


class CheckOut(TemplateView):

    @method_decorator(login_required(login_url="login/"))
    def post(self, request):
        try:
            request.user.subscription
            subscription = stripe.Subscription.retrieve(
                request.user.subscription.stripe_subscription_id)
            return redirect("service")
        except Subscription.DoesNotExist:
            try:
                stripe_customer = stripe.Customer.create(
                    email=request.user.email,
                    source=request.POST['stripeToken'])
                plan = 'price_1H6O7TBfWC4lPABgcU5AD5CA'
                trial_end = datetime.now() + timedelta(days=7)
                trial_end = int(time.mktime(trial_end.timetuple()))
                subscription = stripe.Subscription.create(
                    customer=stripe_customer.id,
                    items=[{'plan': plan}],
                    trial_end=trial_end,)
                customer = Subscription()
                customer.user = request.user
                customer.stripeid = stripe_customer.id
                customer.membership = True
                customer.cancel_at_period_end = False
                customer.state = "trialing"
                customer.stripe_subscription_id = subscription.id
                customer.save()
                return redirect("service")
            except stripe.error.CardError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Your card has been declined'
                )
                return redirect("product")
        except stripe.error.InvalidRequestError:
            try:
                print("we are here")
                stripe_customer = stripe.Customer.retrieve(
                    request.user.subscription.stripeid)
                plan = 'price_1H6O7TBfWC4lPABgcU5AD5CA'
                subscription = stripe.Subscription.create(
                    customer=stripe_customer.id,
                    items=[{'plan': plan}],)
                request.user.subscription.membership = True
                request.user.subscription.cancel_at_period_end = False
                request.user.subscription.stripe_subscription_id = \
                    subscription.id
                request.user.subscription.state = "active"
                request.user.subscription.save()
                return redirect("service")
            except stripe.error.CardError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Your card has been declined'
                )
                redirect("product")

    def get(self, request):
        return redirect("home")


class Cancel(TemplateView):

    @method_decorator(login_required(login_url="login/"))
    def get(self, request):
        try:
            request.user.subscription
            subscription = stripe.Subscription.retrieve(
                request.user.subscription.stripe_subscription_id)
            subscription.cancel_at_period_end = True
            subscription.save()
            request.user.subscription.cancel_at_period_end = True
            request.user.subscription.state = "canceled"
            request.user.subscription.save()
            return redirect("service")
        except Subscription.DoesNotExist:
            return redirect("service")
        except stripe.error.InvalidRequestError:
            request.user.subscription.stripe_subscription_id = ""
            request.user.subscription.state = "not active"
            request.user.subscription.membership = False
            request.user.subscription.save()
            return redirect("service")


class Restart(TemplateView):

    @method_decorator(login_required(login_url="login/"))
    def get(self, request):
        try:
            request.user.subscription
            subscription = stripe.Subscription.retrieve(
                request.user.subscription.stripe_subscription_id)
            subscription.cancel_at_period_end = False
            subscription.save()
            request.user.subscription.state = "active"
            request.user.subscription.cancel_at_period_end = False
            request.user.subscription.save()
            return redirect("service")
        except Subscription.DoesNotExist:
            return ("product")
        except stripe.error.InvalidRequestError:
            return("Product")

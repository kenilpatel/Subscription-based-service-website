from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import Service
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
# Create your views here.


class Home(TemplateView):
    template = "home.html"
    model = Service

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

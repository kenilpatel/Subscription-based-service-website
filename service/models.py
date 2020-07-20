from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# created a service model to store information about the price and name of plan


class Service(models.Model):
    name = models.CharField(max_length=100)
    charges = models.FloatField()


# created subscription model to store information about users subscription


class Subscription(models.Model):
    ''' name of the user having a one to one relationship with default
    user model of django'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ''' state represent the current state of user's subscription
    such as trialing, active cancelled etc'''
    state = models.CharField(max_length=255, default="not active")
    ''' stripe id store stripe id which can be used to fetch
    details of customer from API'''
    stripeid = models.CharField(max_length=255)
    ''' stripe subcription id which can be used to fetch subscription
    details from API'''
    stripe_subscription_id = models.CharField(max_length=255)
    ''' cancel_at_period_end boolean variable store information about
    weather subscription end after billing cycle or not '''
    cancel_at_period_end = models.BooleanField(default=False)
    ''' membership boolean variable is used to store information about
    weather a user is still member or not '''
    membership = models.BooleanField(default=False)

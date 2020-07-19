from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=100)
    charges = models.FloatField()


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)

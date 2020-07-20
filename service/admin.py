from django.contrib import admin
from .models import Service, Subscription
# Register your models here.

# registered our models so this models are visible on default django admin page

admin.site.register(Service)
admin.site.register(Subscription)

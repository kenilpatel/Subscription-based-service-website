# Generated by Django 3.0.8 on 2020-07-20 03:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0003_subscriber_state'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscriber',
            new_name='Subscription',
        ),
    ]

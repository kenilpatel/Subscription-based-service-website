# Generated by Django 3.0.8 on 2020-07-20 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='state',
            field=models.CharField(default='na', max_length=255),
            preserve_default=False,
        ),
    ]

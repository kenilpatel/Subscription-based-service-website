# Generated by Django 3.0.8 on 2020-07-20 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20200719_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='state',
            field=models.CharField(default='Na', max_length=255),
        ),
    ]

# Generated by Django 3.2.7 on 2021-12-09 18:58

from django.db import migrations
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0002_orders_uid'),
        ('app_cart', 'init_delivery_and_payments'),
    ]

    operations = [
        migrations.RemoveField(
         model_name='deliverymethod',
         name='rules',
        ),
        migrations.AddField(
            model_name='deliverymethod',
            name='min_sum',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='min sum'),
        ),
    ]

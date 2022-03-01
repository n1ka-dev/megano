# Generated by Django 3.2.7 on 2021-12-09 19:05

import app_cart.models
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0003_merge_0002_orders_uid_init_delivery_and_payments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='uid'),
        ),
        migrations.AddField(
            model_name='deliverymethod',
            name='max_sum',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='max sum'),
        ),
    ]

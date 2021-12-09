# -*- coding: utf-8 -*-
from django.db import models, migrations

from megano.settings import INITIAL_DELIVERY, INITIAL_PAYMENTS


def set_initial_props(apps, schema_editor):
    settings_model = apps.get_model("app_cart", "DeliveryMethod")
    for code, init_prop in INITIAL_DELIVERY.items():
        # print(code, 'code')
        # print(init_prop, 'init_prop')
        settings_model.objects.create(
            code=code,
            display_name=init_prop['name'],
            price=init_prop['price'],
            rules=init_prop['rules'],
        )
    settings_model = apps.get_model("app_cart", "PaymentMethod")
    for code, name in INITIAL_PAYMENTS:
        settings_model.objects.create(
            code=code,
            display_name=name,
        )


class Migration(migrations.Migration):
    dependencies = [
        ('app_cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverymethod',
            name='code',
            field=models.CharField(max_length=25, null=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='code',
            field=models.CharField(max_length=25, null=True, verbose_name='code'),
        ),
        migrations.RunPython(set_initial_props),
    ]

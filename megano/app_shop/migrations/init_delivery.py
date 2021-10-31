# -*- coding: utf-8 -*-
from django.db import models, migrations

from megano.settings import INITIAL_DELIVERY


def set_initial_props(apps, schema_editor):
    settings_model = apps.get_model("app_cart", "DeliveryMethod")
    for init_prop_name, init_prop in INITIAL_DELIVERY.items():
        settings_model.objects.create(
            name=init_prop_name,
            price=init_prop['price'],
            rules=init_prop['rules'],
        )


class Migration(migrations.Migration):
    dependencies = [
        ('app_shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_initial_props),
    ]

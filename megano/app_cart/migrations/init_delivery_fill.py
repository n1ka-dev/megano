# -*- coding: utf-8 -*-
from django.db import models, migrations

from megano.settings import INITIAL_DELIVERY


def set_initial_props(apps, schema_editor):
    settings_model = apps.get_model("app_cart", "DeliveryMethod")
    for init_prop_name, init_prop in INITIAL_DELIVERY.items():
        settings_model.objects.create(
            code=init_prop_name,
            display_name=init_prop['name'],
            price=init_prop['price'],
            rules=init_prop['rules'],
        )


class Migration(migrations.Migration):
    dependencies = [
        ('app_cart', '0014_auto_20211205_1943'),
    ]

    operations = [
        migrations.RunPython(set_initial_props),
    ]

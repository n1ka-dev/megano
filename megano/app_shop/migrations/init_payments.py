# -*- coding: utf-8 -*-
from django.db import models, migrations

from megano.settings import INITIAL_DELIVERY, INITIAL_PAYMENTS


def set_initial_props(apps, schema_editor):
    settings_model = apps.get_model("app_cart", "PaymentMethod")
    for code, name in INITIAL_PAYMENTS:
        settings_model.objects.create(
            code=code,
            display_name=name
        )


class Migration(migrations.Migration):
    dependencies = [
        ('app_shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_initial_props),
    ]

# -*- coding: utf-8 -*-
from django.db import models, migrations

from megano.settings import INITIAL_PROPS


def set_initial_props(apps, schema_editor):
    settings_model = apps.get_model("app_shop", "SettingsSite")
    for init_prop_name, init_prop_value in INITIAL_PROPS.items():
        settings_model.objects.create(
            name=init_prop_name,
            value=init_prop_value
        )


class Migration(migrations.Migration):
    dependencies = [
        ('app_shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_initial_props),
    ]

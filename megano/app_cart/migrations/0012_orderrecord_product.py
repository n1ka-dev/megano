# Generated by Django 3.2.7 on 2021-11-29 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0011_alter_orderrecord_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderrecord',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_shop.product'),
            preserve_default=False,
        ),
    ]

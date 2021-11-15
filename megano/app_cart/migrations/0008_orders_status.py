# Generated by Django 3.2.7 on 2021-11-11 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0007_auto_20211107_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('payed', 'Paid'), ('payment_error', 'Payment error'), ('draft', 'draft')], default='draft', max_length=50, verbose_name='payment status'),
        ),
    ]

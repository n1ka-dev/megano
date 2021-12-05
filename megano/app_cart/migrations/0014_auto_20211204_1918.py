# Generated by Django 3.2.7 on 2021-12-04 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0013_alter_orderrecord_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, null=True, verbose_name='code')),
                ('display_name', models.CharField(max_length=15, null=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'payment method',
                'verbose_name_plural': 'payment methods',
                'db_table': 'payment_methods',
                'ordering': ('id',),
            },
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_cart.paymentmethod', verbose_name='payment method'),
        ),
    ]

# Generated by Django 3.2.7 on 2021-09-25 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='views count'),
        ),
    ]
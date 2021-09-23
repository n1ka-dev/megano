# Generated by Django 3.2.7 on 2021-09-22 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210922_2301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='desc',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='desc',
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True, null=True, verbose_name='short description'),
        ),
    ]

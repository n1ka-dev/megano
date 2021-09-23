# Generated by Django 3.2.7 on 2021-09-22 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210922_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='uploads/category/icons/'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True, verbose_name='slug'),
        ),
    ]
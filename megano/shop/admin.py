from django.contrib import admin
from shop.models import Product, Category, Image, Tags


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['name', 'short_description', 'price']
    search_fields = ['name', 'short_description']


@admin.register(Tags)
class Tags(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(Image)
class Image(admin.ModelAdmin):
    list_display = ['title', 'alt']
    search_fields = ['title', 'alt']


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['name', 'description', 'slug', 'parent_category', 'icon']
    search_fields = ['name', 'description']

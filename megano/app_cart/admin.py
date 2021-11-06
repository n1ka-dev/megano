from django.contrib import admin

from app_cart.models import DeliveryMethod, Orders


@admin.register(DeliveryMethod)
class DeliveryMethod(admin.ModelAdmin):
    list_display = ['code', 'price', 'rules']
    search_fields = ['code', 'price']


@admin.register(Orders)
class Orders(admin.ModelAdmin):
    list_display = ['city', 'address', 'phone', 'paid']
    search_fields = ['id', 'city', 'address', 'phone']

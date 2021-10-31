from django.contrib import admin

from app_cart.models import DeliveryMethod


@admin.register(DeliveryMethod)
class DeliveryMethod(admin.ModelAdmin):
    list_display = ['code', 'price', 'rules']
    search_fields = ['code', 'price']
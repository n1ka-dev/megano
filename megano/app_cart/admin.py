from django.contrib import admin

from app_cart.models import DeliveryMethod, Orders, OrderRecord


class OrderRecordTabular(admin.TabularInline):
    model = OrderRecord


@admin.register(DeliveryMethod)
class DeliveryMethod(admin.ModelAdmin):
    list_display = ['code', 'price', 'rules']
    search_fields = ['code', 'price']


@admin.register(Orders)
class Orders(admin.ModelAdmin):
    inlines = (OrderRecordTabular,)
    list_display = ['id', 'uid', 'city', 'address', 'phone', 'create_date', 'status']
    search_fields = ['uid', 'city', 'address', 'phone']

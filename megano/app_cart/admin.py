from django.contrib import admin

from app_cart.models import DeliveryMethod, Orders, OrderRecord, PaymentMethod


class OrderRecordTabular(admin.TabularInline):
    model = OrderRecord


# @admin.register(DeliveryMethod)
# class DeliveryMethod(admin.ModelAdmin):
#     # list_display = ['code', 'price', 'min_sum', 'max_sum', 'display_name']
    # search_fields = ['code', 'price']


@admin.register(PaymentMethod)
class PaymentMethod(admin.ModelAdmin):
    list_display = ['code']
    search_fields = ['code', 'display_name']


@admin.register(Orders)
class Orders(admin.ModelAdmin):
    inlines = (OrderRecordTabular,)
    # list_display = ['id', 'uid', 'city', 'address', 'phone', 'create_date', 'status']
    # search_fields = ['uid', 'city', 'address', 'phone']

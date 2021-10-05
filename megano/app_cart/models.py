from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_shop.models import Product


class Cart(models.Model):
    goods = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order = models.ForeignKey('Orders', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'cart'
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class Orders(models.Model):
    address = models.CharField(max_length=250, verbose_name=_('address'))
    phone = models.CharField(max_length=15, verbose_name=_('phone'), null=True)
    receiver_name = models.CharField(max_length=50, verbose_name=_('receiver name'), null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), null=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('create date'))

    class Meta:
        db_table = 'orders'
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-create_date',)

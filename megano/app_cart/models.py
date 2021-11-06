from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_shop.models import Product
from megano.settings import PAYMENT_CHOICES


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


class DeliveryMethod(models.Model):
    code = models.CharField(max_length=15, verbose_name=_('code'), null=True)
    display_name = models.CharField(max_length=15, verbose_name=_('name'), null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    rules = models.CharField(max_length=150, verbose_name=_('rules'), null=True)

    class Meta:
        db_table = 'delivery_methods'
        verbose_name = _('delivery method')
        verbose_name_plural = _('delivery methods')
        ordering = ('id',)


class Orders(models.Model):
    city = models.CharField(max_length=15, verbose_name=_('city'), null=True)
    address = models.CharField(max_length=250, verbose_name=_('address'))
    phone = models.CharField(max_length=15, verbose_name=_('phone'), null=True)
    receiver_name = models.CharField(max_length=50, verbose_name=_('receiver name'), null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), null=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('create date'))
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE, verbose_name=_('delivery method'),
                                        default=None)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='p', verbose_name=_('payment method'))
    paid = models.BooleanField(default=False, verbose_name=_('paid'))

    class Meta:
        db_table = 'orders'
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-create_date',)

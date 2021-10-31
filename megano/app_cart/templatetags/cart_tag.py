from django import template

from app_cart.CartService import CartService
from megano.settings import CUSTOM_DELIVERY_PROPERTY_NAME, EXPRESS_DELIVERY_PROPERTY_NAME, \
    MIN_AMOUNT_TO_FREE_DELIVERY_PROPERTY_NAME

register = template.Library()


@register.simple_tag()
def get_total_price_cart(request, *args, **kwargs):
    """
    Подсчет стоимости товаров в корзине.
    """
    cart = CartService(request)
    return cart.get_sum()


@register.simple_tag()
def get_express_delivery_price(request, *args, **kwargs):
    # price = SettingsSite.objects.get(name=EXPRESS_DELIVERY_PROPERTY_NAME).value
    return 0


@register.simple_tag()
def get_delivery_price(request, *args, **kwargs):
    cart_total = get_total_price_cart(request)
    # min_sum_for_free_delivery = SettingsSite.objects.get(name=MIN_AMOUNT_TO_FREE_DELIVERY_PROPERTY_NAME)
    price = 0
    # if cart_total <= float(min_sum_for_free_delivery.value):
    #     price = SettingsSite.objects.get(name=CUSTOM_DELIVERY_PROPERTY_NAME).value
    return price


@register.simple_tag()
def get_count_position_cart(request, *args, **kwargs):
    """
    Подсчет товаров в корзине.
    """
    cart = CartService(request)

    return cart.get_count()

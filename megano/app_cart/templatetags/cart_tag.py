from django import template

from app_cart.CartService import CartService

register = template.Library()


@register.simple_tag()
def get_total_price_cart(request, *args, **kwargs):
    """
    Подсчет стоимости товаров в корзине.
    """
    cart = CartService(request)
    return cart.get_sum()


@register.simple_tag()
def get_count_position_cart(request, *args, **kwargs):
    """
    Подсчет товаров в корзине.
    """
    cart = CartService(request)

    return cart.get_count()

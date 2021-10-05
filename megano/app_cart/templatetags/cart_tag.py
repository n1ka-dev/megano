from django import template
from django.db.models import Sum, F
from django.utils.safestring import mark_safe
from app_cart.models import Cart
from megano import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_total_price_cart(context, *args, **kwargs):
    """
    Подсчет стоимости товаров в корзине.
    """
    session = context.request.session
    cart = session.get(settings.CART_SESSION_ID)
    return sum(float(item['price']) * item['quantity'] for item in
               cart.values())


@register.simple_tag(takes_context=True)
def get_count_position_cart(context, *args, **kwargs):
    """
    Подсчет товаров в корзине.
    """
    session = context.request.session
    cart = session.get(settings.CART_SESSION_ID)
    print(session)
    return len(cart)

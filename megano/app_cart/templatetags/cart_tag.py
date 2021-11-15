from django import template
from django.utils.safestring import mark_safe

from app_cart.CartService import CartService
from app_cart.models import Orders

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
    # cart_total = get_total_price_cart(request)
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


@register.simple_tag(takes_context=True)
def get_status_section(context, *args, **kwargs):
    """
    Подсчет товаров в корзине.
    """
    status = Orders.objects.get(uid=context.get('uid')).status
    if status == Orders.PAYMENT_ERROR:
        html = "<div class=\"ProgressPayment\">" \
               f"<div class=\"ProgressPayment-title\">{ Orders.PAYMENT_ERROR_MESSAGE }</div>" \
               """<div class="ProgressPayment-icon">
               <img src="/assets/img/icons/stop.png">
              </div>
            </div>"""
    elif status == Orders.PAID:
        html = "<div class=\"ProgressPayment\">" \
               f"<div class=\"ProgressPayment-title\">{ Orders.PAID_MESSAGE }</div>" \
               """<div class="ProgressPayment-icon">
               <img src="/assets/img/icons/86784775.gif">
              </div>
            </div>"""
    else:
        html = "<div class=\"ProgressPayment\">" \
               f"<div class=\"ProgressPayment-title\">{ Orders.CUSTOM_MESSAGE }</div>" \
               """<div class="ProgressPayment-icon">
                <div class="cssload-thecube">
                  <div class="cssload-cube cssload-c1"></div>
                  <div class="cssload-cube cssload-c2"></div>
                  <div class="cssload-cube cssload-c4"></div>
                  <div class="cssload-cube cssload-c3"></div>
                </div>
              </div>
            </div>"""
    return mark_safe(html)

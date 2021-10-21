from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from app_cart.templatetags.cart_tag import get_total_price_cart, get_count_position_cart, CartService
from app_shop.models import Product
from django.views.generic import FormView, TemplateView

from app_cart.forms import CheckoutForm

TYPE_OPERATION_ADD = 'add'
TYPE_OPERATION_REMOVE = 'remove'
TYPE_OPERATION_SET = 'remove'


def cart_update(request, product_id):
    cart = CartService(request)
    product = get_object_or_404(Product, id=product_id)
    count = request.POST.get('count', 0)
    count = int(count)
    if count and request.method == 'POST':
        update = request.POST.get('update', False)
        cart.add(product=product, count=count, update_quantity=update)
        if update:
            status = _('updated')
        else:
            status = _('added')
        return HttpResponse(JsonResponse({'status': 'success', "amount_sum": get_total_price_cart(request),
                                          "amount_count": get_count_position_cart(request),
                                          'message': _(f'Product {product.name} '
                                                       f'successfully {status}')}))
    else:
        cart.remove(product)
        return HttpResponse(JsonResponse({'status': 'success', "amount_sum": get_total_price_cart(request),
                                          "amount_count": get_count_position_cart(request),
                                          'message': _(f'Product {product.name} '
                                                       'successfully removed')}))


def cart_detail(request):
    cart = CartService(request)
    return render(request, 'cart.html', {'cart_list': cart})


# TODO дублирование кода. подумать как убрать
def products_in_cart(request):
    cart = CartService(request)
    return render(request, 'products_in_cart.html', {'cart_list': cart})


class CheckoutView(TemplateView, FormView):
    form_class = CheckoutForm
    template_name = 'checkout.html'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from django.utils.translation import gettext_lazy as _
from app_cart.models import Cart
from app_shop.models import Product
from megano import settings


@require_POST
def cart_add(request, product_id):
    cart = CartService(request)
    product = get_object_or_404(Product, id=product_id)
    count = request.POST.get('count')
    cart.add(product=product,
             count=count)
    return HttpResponse(JsonResponse({'status': 'sucess', "code": 200, 'message': _('Successfully added')}))


class CartService:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, count=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = float(count)
        else:
            self.cart[product_id]['quantity'] += float(count)
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


class CartView(LoginRequiredMixin, ListView):
    model = Cart
    login_url = reverse_lazy('login')
    template_name = 'cart.html'
    context_object_name = 'cart_list'

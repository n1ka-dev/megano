from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import SingleObjectMixin

from app_cart.OrderService import OrderService
from app_cart.models import DeliveryMethod, Orders
from app_cart.templatetags.cart_tag import get_total_price_cart, get_count_position_cart, CartService
from app_shop.models import Product
from django.views.generic import FormView, TemplateView, CreateView, DetailView

from app_cart.forms import CheckoutForm, PayForm
from app_users.forms import RegisterForm, AuthForm

TYPE_OPERATION_ADD = 'add'
TYPE_OPERATION_REMOVE = 'remove'
TYPE_OPERATION_SET = 'remove'


def save_order_info(request):
    fio = request.POST.get('fio', False)
    phone = request.POST.get('phone', False)
    address = request.POST.get('address', False)
    city = request.POST.get('city', False)
    payment_method = request.POST.get('payment_method', False)
    delivery_method = request.POST.get('delivery_method', False)
    data = {
        'f-row': {
            'fio': fio,
            'phone': phone,
            'address': address
        },
        's-row': {
            'city': city,
            'payment_method': payment_method,
            'delivery_method': delivery_method,
        }
    }

    order = OrderService(request)
    order.save(data)
    return HttpResponse(JsonResponse({'status': 'success',
                                      'html': order.get_html(),
                                      'message': _(f'order info saved')}))


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


class PayWaitView(TemplateView, FormView):
    template_name = 'progressPayment.html'
    form_class = PayForm


class PayView(TemplateView, FormView):
    template_name = 'payment.html'
    form_class = PayForm

    def get_success_url(self):
        return reverse('pay-wait', kwargs={'uid': self.kwargs['uid']})


class CheckoutView(TemplateView, FormView):
    template_name = 'checkout.html'
    # model = Orders
    upid = None

    def get_success_url(self):
        return reverse('pay', kwargs={'uid': self.uid})

    def get(self, *args, **kwargs):
        cart = CartService(self.request)
        if not len(cart) or len(cart) == 0:
            return HttpResponseRedirect(reverse_lazy('cart'))
        return super().get(self.request, *args, **kwargs)

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return CheckoutForm
        elif self.request.GET.get('already_register', False):
            return AuthForm
        else:
            return RegisterForm

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        cart = CartService(self.request)

        context['cart_list'] = cart
        return context

    def get_form(self, form_class=None):
        form = super(CheckoutView, self).get_form(form_class)
        if 'fio' in form.fields and self.request.user.is_authenticated:
            form.fields['fio'].initial = ' '.join([self.request.user.last_name,
                                                   self.request.user.first_name])

        if 'phone' in form.fields and self.request.user.is_authenticated:
            form.fields['phone'].initial = self.request.user.profile.phone

        if 'email' in form.fields and self.request.user.is_authenticated:
            form.fields['email'].initial = self.request.user.email

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        code = form.cleaned_data.get('delivery_method')
        form.instance.delivery_method = DeliveryMethod.objects.get(code=code)
        order = form.save()

        self.uid = order.uid
        return super().form_valid(form)

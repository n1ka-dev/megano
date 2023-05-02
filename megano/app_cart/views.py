from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

from app_cart.OrderService import OrderService
from app_cart.models import DeliveryMethod, Orders, OrderRecord, PaymentMethod
from app_cart.templatetags.cart_tag import get_total_price_cart, get_count_position_cart, CartService
from app_shop.models import Product
from django.views.generic import FormView, TemplateView, CreateView, DetailView, UpdateView

from app_cart.forms import CheckoutForm, PayForm
from app_users.forms import RegisterForm, AuthForm
from app_cart.tasks import pay_service_emulation

TYPE_OPERATION_ADD = 'add'
TYPE_OPERATION_REMOVE = 'remove'
TYPE_OPERATION_SET = 'remove'


def save_order_info(request):
    fio = request.POST.get('fio', False)
    uid = request.POST.get('uid', False)
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
    cart = CartService(request, uid)
    order.save(data)
    return HttpResponse(JsonResponse({'status': 'success',
                                      'html': order.get_html(),
                                      'delivery_price': order.delivery_method.price,
                                      'total_price': "{:.2f}".format(
                                          float(order.delivery_method.price) + cart.get_sum()),
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


def products_in_cart(request):
    cart = CartService(request)
    return render(request, 'products_in_cart.html', {'cart_list': cart})


class PayWaitView(TemplateView):
    template_name = 'progressPayment.html'


def get_status_order(request, uid):
    status = Orders.objects.get(uid=uid).status
    message = _('We are waiting for confirmation of payment by the payment system')
    if status == Orders.PAID:
        message = _('Order successfully paid')
    if status == Orders.PAYMENT_ERROR:
        message = _('Payment declined')
    return HttpResponse(JsonResponse({'status': status, 'message': message}))


class OrderDetailView(DetailView):
    model = Orders
    template_name = 'oneorder.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['need_pay_form'] = False if context['object'].status == Orders.PAID else True
        return context


class PayView(TemplateView, FormView):
    template_name = 'payment.html'
    form_class = PayForm

    def get_success_url(self):
        return reverse('pay-wait', kwargs={'uid': self.kwargs['uid']})

    def form_valid(self, form):
        cart_number = form.cleaned_data.get('cart_number')
        pay_service_emulation.delay(cart_number, self.kwargs['uid'])
        cart = CartService(self.request)
        cart.clear()
        return super().form_valid(form)


class CheckoutView(TemplateView, FormView):
    template_name = 'checkout.html'
    upid = None

    def get_success_url(self):
        return reverse('pay', kwargs={'uid': self.uid})

    def get(self, *args, **kwargs):
        cart = CartService(self.request)
        if not len(cart) or len(cart) == 0:
            return HttpResponseRedirect(reverse_lazy('cart'))
        return super().get(self.request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            cart = CartService(self.request)
            sum_cart = cart.get_sum()
            kwargs['sum_cart'] = sum_cart
        return kwargs

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
        context['action_url'] = reverse('checkout')

        return context

    def get_form(self, form_class=None):
        form = super(CheckoutView, self).get_form(form_class)
        if 'receiver_name' in form.fields and self.request.user.is_authenticated:
            form.fields['receiver_name'].initial = ' '.join([self.request.user.last_name,
                                                             self.request.user.first_name])

        if 'phone' in form.fields and self.request.user.is_authenticated:
            form.fields['phone'].initial = self.request.user.profile.phone

        if 'email' in form.fields and self.request.user.is_authenticated:
            form.fields['email'].initial = self.request.user.email

        return form

    def form_invalid(self, form):

        for field in form.errors:
            print(field)

        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user

        code_d = form.cleaned_data.get('delivery_method')
        form.instance.delivery_method = DeliveryMethod.objects.get(code=code_d)

        code_p = form.cleaned_data.get('payment_method')
        form.instance.payment_method = PaymentMethod.objects.get(code=code_p)
        order = form.save()
        self.uid = order.uid
        cart = CartService(self.request)
        for item in cart:
            OrderRecord.objects.create(
                product_name=item['product']['name'],
                count=item['quantity'],
                price=item['product']['price'],
                product_id=item['product']['id'],
                order=order
            )
        return super().form_valid(form)


class ContinueCheckoutView(UpdateView):
    model = Orders
    form_class = CheckoutForm
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super(ContinueCheckoutView, self).get_context_data(**kwargs)
        cart = CartService(self.request, context['object'].uid)
        context['cart_list'] = cart
        context['action_url'] = reverse('continue-checkout', kwargs={'pk': context['object'].id})

        return context

    def get_form_kwargs(self):
        kwargs = super(ContinueCheckoutView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            cart = CartService(self.request, self.object.uid)
            sum_cart = cart.get_sum()
            kwargs['sum_cart'] = sum_cart
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'email' in form.fields and self.request.user.is_authenticated:
            form.fields['email'].initial = self.request.user.email

        return form

    def get_success_url(self):
        return reverse('pay', kwargs={'uid': self.object.uid})

    def form_valid(self, form):
        code_d = form.cleaned_data.get('delivery_method')
        form.instance.delivery_method = DeliveryMethod.objects.get(code=code_d)

        code_p = form.cleaned_data.get('payment_method')
        form.instance.payment_method = PaymentMethod.objects.get(code=code_p)
        form.instance.status = Orders.DRAFT
        form.save()

        return super().form_valid(form)

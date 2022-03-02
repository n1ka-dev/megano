from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from app_cart.CartService import CartService
from app_cart.models import Orders, DeliveryMethod, PaymentMethod


class PayForm(forms.Form):
    cart_number = forms.CharField(label=_('Cart number'),
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-input', 'data-validate': 'require pay',
                                             'data-mask': '9999 9999', 'placeholder': '9999 9999'}),
                                  error_messages={'required': _('Enter cart number')})

    def clean_cart_number(self):
        cart_number = int(self.cleaned_data['cart_number'].replace(' ', ''))
        return cart_number


class CheckoutForm(forms.ModelForm):
    receiver_name = forms.CharField(max_length=50, label=_('FIO'),
                                    widget=forms.TextInput(attrs={'class': 'form-input', 'data-validate': 'require'}),
                                    error_messages={'required': _('Enter your Name')})
    phone = forms.CharField(max_length=50, label=_('Phone'),
                            widget=forms.TextInput(attrs={'class': 'form-input', 'data-validate': 'require'}),
                            error_messages={'required': _('Enter your phone')})
    email = forms.CharField(max_length=50, label='Email', widget=forms.TextInput(attrs={'class': 'form-input', 'data'
                                                                                                               '-validate': 'require'}),
                            error_messages={'required': _('Enter your email address')})
    city = forms.CharField(max_length=50, label='City', widget=forms.TextInput(attrs={'class': 'form-input', 'data'
                                                                                                             '-validate': 'require'}),
                           error_messages={'required': _('Enter your city')})
    address = forms.CharField(max_length=50, label='Address',
                              widget=forms.Textarea(attrs={'class': 'form-textarea', 'data-validate': 'require'}),
                              error_messages={'required': _('Enter your address')})
    delivery_method = forms.ChoiceField(choices=(), widget=forms.RadioSelect )
    payment_method = forms.ChoiceField(choices=(), widget=forms.RadioSelect, initial='online', )

    class Meta:
        model = Orders
        fields = ['receiver_name', 'address', 'city', 'email', 'phone']

    def __init__(self, sum_cart=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['delivery_method'].choices = [(item.code, item.display_name) for item in
                                                  DeliveryMethod.objects.filter(
                                                      Q(min_sum__lt=sum_cart) | Q(max_sum__gte=sum_cart) | Q(
                                                          min_sum__isnull=True, max_sum__isnull=True))]
        initial_delivery_code = 'free_price'
        if initial_delivery_code not in dict(self.fields['delivery_method'].choices):
            initial_delivery_code = 'delivery_price'

        self.fields['delivery_method'].initial = initial_delivery_code
        self.fields['payment_method'].choices = [(item.code, item.display_name) for item in PaymentMethod.objects.all()]

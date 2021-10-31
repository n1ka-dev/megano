from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from app_cart.models import Orders, DeliveryMethod


class CheckoutForm(forms.Form):
    DELIVERY_CHOICES = [(item.code, item.display_name) for item in DeliveryMethod.objects.all()]
    PAYMENT_CHOICES = [
                        ('cart', _('Online cart')),
                        ('random_account', _('Online from a random account')),
                       ]

    fio = forms.CharField(max_length=50, label=_('FIO'), widget=forms.TextInput(attrs={'class': 'form-input', 'data-validate':'require'}),
                          error_messages={'required': _('Enter your Name')})
    phone = forms.CharField(max_length=50, label=_('Phone'), widget=forms.TextInput(attrs={'class': 'form-input', 'data-validate':'require'}),
                            error_messages={'required': _('Enter your phone')})
    email = forms.CharField(max_length=50, label='Email', widget=forms.TextInput(attrs={'class': 'form-input', 'data'
                                                                                                               '-validate':'require'}),
                            error_messages={'required': _('Enter your email address')})
    city = forms.CharField(max_length=50, label='City', widget=forms.TextInput(attrs={'class': 'form-input', 'data'
                                                                                                             '-validate':'require'}),
                           error_messages={'required': _('Enter your city')})
    address = forms.CharField(max_length=50, label='Address', widget=forms.Textarea(attrs={'class': 'form-textarea', 'data-validate':'require'}),
                              error_messages={'required': _('Enter your address')})
    delivery_method = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect, initial='free_price',)
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect, initial='cart',)

    class Meta:
        model = Orders
        fields = ['delivery_method', 'address', 'city', 'email', 'phone', 'fio']

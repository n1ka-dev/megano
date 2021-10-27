from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class RegisterForm(UserCreationForm):
    fio = forms.CharField(max_length=50, label=_('FIO'), widget=forms.TextInput(attrs={'class': 'form-input'}),
                          error_messages={'required': _('Enter your Name')})
    phone = forms.CharField(max_length=50, label=_('Phone'), widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={'required': _('Enter your phone')})
    email = forms.CharField(max_length=50, label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={'required': _('Enter your email address')})
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label=_('Confirm password'))


class CheckoutForm(forms.Form):
    fio = forms.CharField(max_length=50, label=_('FIO'), widget=forms.TextInput(attrs={'class': 'form-input'}),
                          error_messages={'required': _('Enter your Name')})
    phone = forms.CharField(max_length=50, label=_('Phone'), widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={'required': _('Enter your phone')})
    email = forms.CharField(max_length=50, label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={'required': _('Enter your email address')})


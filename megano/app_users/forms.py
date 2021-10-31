from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    fio = forms.CharField(max_length=50, label=_('FIO'), widget=forms.TextInput(attrs={'class': 'form-input'}),
                          error_messages={'required': _('Enter your Name')})
    phone = forms.CharField(max_length=50, label=_('Phone'), widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={'required': _('Enter your phone')})
    email = forms.CharField(max_length=50, label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={'required': _('Enter your email address')})
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label=_('Confirm password'))

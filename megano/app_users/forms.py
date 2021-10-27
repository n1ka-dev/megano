from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='ФИО', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'ФИО', 'class': 'form-input'}))

    phone = forms.CharField(label='Телефон', max_length=30, required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'form-input'}))
    username = forms.CharField(label='E-mail', max_length=30,
                               widget=forms.TextInput(attrs={'placeholder': 'E-mail', 'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', max_length=30,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Тут можно изменить пароль', 'class': 'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля', max_length=30,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль повторно', 'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')

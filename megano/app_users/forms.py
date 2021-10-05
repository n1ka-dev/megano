from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    avatar = forms.FileField(label='Аватар', required=False, )

    first_name = forms.CharField(label='Имя', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', max_length=30,
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    city = forms.CharField(label='Город', max_length=30, required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Город'}))
    phone = forms.CharField(label='Телефон', max_length=30, required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'Телефон'}))
    username = forms.CharField(label='Логин', max_length=30,
                               widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password1 = forms.CharField(label='Пароль', max_length=30,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', max_length=30,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

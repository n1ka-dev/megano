from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    fio = forms.CharField(max_length=50, label=_('FIO'),
                          widget=forms.TextInput(attrs={'class': 'form-input', 'data-validate': 'require'}),
                          error_messages={'required': _('Enter your Name')})
    phone = forms.CharField(max_length=50, label=_('Phone'), widget=forms.TextInput(
        attrs={'class': 'form-input', 'type': 'tel', 'data-validate': 'require'}),
                            error_messages={'required': _('Enter your phone')})

    username = forms.EmailField(max_length=50, label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-input', 'type': 'email', 'data-validate': 'require'}),
                                error_messages={'required': _('Enter your email address')})
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'type': 'password', 'placeholder': 'Тут можно изменить пароль'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'type': 'password', 'placeholder': 'Введите пароль повторно'}),
    )


class ProfileEditForm(forms.ModelForm):
    avatar = forms.FileField(label=_('Choose an avatar'), required=False,
                              widget=forms.ClearableFileInput(attrs={'class': 'Profile-file form-input'}))

    last_name = forms.CharField(max_length=50, label=_('FIO'),
                                widget=forms.TextInput(attrs={'class': 'form-input', 'data-validate': 'require'}),
                                error_messages={'required': _('Enter your Name')})

    email = forms.EmailField(max_length=50, label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-input', 'type': 'email', 'data-validate': 'require'}),
                             error_messages={'required': _('Enter your email address')})

    phone = forms.CharField(max_length=50, label=_('Phone'), widget=forms.TextInput(
        attrs={'class': 'form-input', 'type': 'tel', 'data-validate': 'require'}),
                            error_messages={'required': _('Enter your phone')})
    password = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'type': 'password', 'placeholder': 'Тут можно изменить пароль'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        required=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'type': 'password', 'placeholder': 'Введите пароль повторно'}),
    )

    class Meta:
        model = User
        fields = ('last_name', 'email', 'password')

    def clean(self):
        cleaned_data = super(ProfileEditForm, self).clean()

        password = cleaned_data.get("password")
        avatar = cleaned_data.get("avatar")
        if not avatar:
            del cleaned_data['avatar']
        if not password:
            del cleaned_data['password']
        else:
            confirm_password = cleaned_data.get("password2")
            if password != confirm_password:
                raise forms.ValidationError(
                    "password and confirm_password does not match"
                )
            else:
                cleaned_data['password'] = make_password(cleaned_data['password'])
        return cleaned_data

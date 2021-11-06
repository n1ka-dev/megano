from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from app_users.forms import AuthForm, RegisterForm
from app_users.models import Profile


class SiteAuthUser(LoginView):
    template_name = 'users/login.html'
    form_class = AuthForm

    # TODO если в корзине, то в корзину кидать
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main'))
        return super().get(self.request, *args, **kwargs)


class SiteRegistrationUserView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main'))
        return super().get(self.request, *args, **kwargs)

    def get_success_url(self):
        # TODO если в корзине, то в корзину кидать
        return reverse_lazy('main')

    def form_valid(self, form):
        form.instance.email = form.cleaned_data.get('username')
        form.instance.last_name = form.cleaned_data.get('fio')
        user = form.save()
        phone = form.cleaned_data.get('phone')

        Profile.objects.create(
            user=user,
            phone=phone
        )

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            print('авторизовался....')
        else:
            print('не получилось авторизоваться....')
        return super().form_valid(form)

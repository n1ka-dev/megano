from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from app_users.forms import AuthForm


class AuthUser(LoginView):
    template_name = 'login.html'
    form_class = AuthForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main'))
        return super().get(self.request, *args, **kwargs)

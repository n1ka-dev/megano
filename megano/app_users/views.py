from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView, TemplateView, ListView

from app_cart.models import Orders
from app_users.forms import AuthForm, RegisterForm, ProfileEditForm
from app_users.models import Profile


class SiteAuthUser(LoginView):
    template_name = 'users/login.html'
    form_class = AuthForm

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


class SiteLogoutView(LogoutView):
    template_name = 'users/logout.html'


class AccountUserView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountUserView, self).get_context_data(**kwargs)
        context['last_order'] = Orders.objects.filter(user=self.request.user).order_by('-create_date')[:1]
        print(context)
        return context


class HistoryOrdersView(LoginRequiredMixin, ListView):
    model = Orders
    template_name = 'users/historyorder.html'


class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/profile.html'

    def get_form(self, form_class=None):
        form = super(ProfileUserView, self).get_form(form_class)
        form.fields['phone'].initial = self.request.user.profile.phone
        form.fields['email'].initial = self.request.user.email

        return form

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self):
        user = self.request.user
        return user

    def form_valid(self, form):
        phone = form.cleaned_data.get('phone')
        avatar = form.cleaned_data.get('avatar')
        kwargs = {'phone': phone}
        if avatar:
            fs = FileSystemStorage(location='uploads/avatars', base_url='uploads/avatars')
            filename = fs.save(avatar.name, avatar)
            kwargs['avatar'] = fs.url(filename)

        user = self.get_object()
        Profile.objects.filter(user=user).update(**kwargs)
        password = form.cleaned_data.get('password')
        if password:
            update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)

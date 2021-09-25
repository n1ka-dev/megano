from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView
from shop.models import Product
from shop.forms import CommentForm


class CatalogView(ListView):
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'catalog'
    paginate_by = 8


class ProductDetailView(DetailView, FormView):
    model = Product
    form_class = CommentForm
    template_name = 'product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):
        item = super().get_object()
        return item

    def get_success_url(self):
        return reverse('product-detail', kwargs={'slug': self.kwargs['slug']})

    def get_form(self, form_class=None):
        form = super(ProductDetailView, self).get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields.pop('nickname')
            form.fields.pop('email')

        return form

    def form_valid(self, form):
        self.object = self.get_object()
        if isinstance(self.request.user, User):
            form.instance.author = self.request.user
        form.instance.product_id = self.object.id
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = self.get_object()
        print(form.errors)
        return super().form_invalid(form)

from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from shop.models import Product


class CatalogView(ListView):
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'catalog'
    paginate_by = 8


class ProductDetailView(DetailView): #FormView
    model = Product
    template_name = 'product.html'
    # form_class = CommentForm
    context_object_name = 'product'


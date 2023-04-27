from django.contrib.auth.models import User
from django.db.models import F, Count
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView
from rest_framework.generics import ListCreateAPIView

from app_shop.models import Product, Comment, Tags
from app_shop.forms import CommentForm
from app_shop.serializer import CommentSerializer


class CatalogView(ListView):
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'catalog'

    paginate_by = 8
    sorting_fields = {
        'popular': 'views_count',
        'price': 'price',
        'create_date': 'create_date',
        'reviews': 'reviews',
    }

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('images', 'tags').filter(published=True)

        if 'category_slug' in self.kwargs:
            qs = qs.filter(category__slug=self.kwargs['category_slug'])

        title = self.request.GET.get('title')
        if title:
            qs = qs.filter(name__icontains=title[1:])

        price = self.request.GET.get('price')
        if price:
            price_start, price_end = price.split(';')
            qs = qs.filter(price__gte=price_start, price__lte=price_end)
        in_stock = self.request.GET.get('stock_balance')
        if in_stock:
            qs = qs.filter(stock_balance__gte=0)
        sort_field = self.request.GET.get('sort_field', 'popular')
        sort_by = self.request.GET.get('sort_by', 'inc')
        pref = '-' if sort_by == 'dec' else ''

        if sort_field != 'reviews':
            qs = qs.order_by(f'{pref}{self.sorting_fields[sort_field]}')
        else:
            qs = qs.annotate(cnt=Count('comment')).order_by(f'{pref}cnt')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_ordered = Product.objects.all().order_by('price')
        context['min_price'], context['max_price'] = qs_ordered.first().price, qs_ordered.last().price
        price = self.request.GET.get('price')
        context['free_delivery'] = 'checked' if self.request.GET.get('free_delivery') else ''
        context['in_stock'] = 'checked' if self.request.GET.get('in_stock') else ''

        if price:
            context['min_price_set'], context['max_price_set'] = price.split(';')
        else:
            context['min_price_set'], context['max_price_set'] = context['min_price'], context['max_price']

        return context


class ProductDetailView(DetailView, FormView):
    model = Product
    slug_url_kwarg = "product_slug"
    slug_field = "slug"

    form_class = CommentForm
    template_name = 'product.html'
    context_object_name = 'product'
    queryset = Product.objects.only('name', 'description', 'price', 'slug') \
        .prefetch_related('images')

    def get(self, request, *args, **kwargs):
        slug = kwargs['product_slug']
        Product.objects.filter(slug=slug).update(views_count=F('views_count') + 1)
        item = super().get(request, {'slug': slug})
        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comments'] = Comment.objects.filter(product__slug=self.kwargs['product_slug']).select_related('author') \
            .annotate(username=F('author__username')).filter(status='p').order_by('-id')
        context['count_comments'] = len(context['comments'])
        return context

    def get_success_url(self):
        return reverse('product-detail', kwargs={'slug': self.kwargs['product_slug']})

    def get_form(self, form_class=None):
        form = super(ProductDetailView, self).get_form(form_class)

        return form

    def form_valid(self, form):
        if isinstance(self.request.user, User):
            form.instance.author = self.request.user
        form.instance.product = Product.objects.get(slug=self.kwargs['slug'])
        form.save()
        return super().form_valid(form)


class CommentAdd(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs['slug'])
        kwargs = {'product': product}
        if isinstance(self.request.user, User):
            kwargs['author'] = self.request.user
        serializer.save(**kwargs)


def comments_list(request, slug):
    comments = Comment.objects.filter(product__slug=slug).order_by('-id')
    response = render(
        request,
        'comments_product.html',
        {
            'comments': comments
        }
    )

    return response

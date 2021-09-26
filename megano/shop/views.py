from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView
from shop.models import Product, Comment
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
    queryset = Product.objects.only('name', 'description', 'price', 'slug') \
        .prefetch_related('images')

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        Product.objects.filter(slug=slug).update(views_count=F('views_count') + 1)
        item = super().get(request, {'slug': slug})
        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment'] = Comment.objects.filter(product__slug=self.kwargs['slug']).select_related('author')\
            .annotate(username=F('author__username')).filter(status='p')
        context['comment_count'] = len(context['comment'])
        return context

    def get_object(self, *args, **kwargs):
        item = super().get_object()
        print(item, 'get_object')
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

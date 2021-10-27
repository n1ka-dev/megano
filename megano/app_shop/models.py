from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from pytils.translit import slugify
from django.utils.translation import gettext_lazy as _


class SettingsSite(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('name'))
    value = models.CharField(max_length=250, verbose_name=_('value'))

    class Meta:
        db_table = 'settings'
        verbose_name = _('settings')
        verbose_name_plural = _('settings')


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('name'))
    slug = models.SlugField(max_length=250, verbose_name=_('slug'), blank=True, unique=True)
    parent_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name=_('parent category'))
    icon = models.FileField(upload_to='uploads/category/icons/', null=True, blank=True)
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)


class Tags(models.Model):
    name = models.CharField(max_length=170, verbose_name=_('name'))
    description = models.CharField(max_length=170, verbose_name=_('description'), blank=True)

    class Meta:
        db_table = 'tags'
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.FileField(upload_to='uploads/images/')
    alt = models.CharField(max_length=50, verbose_name=_('alt'))
    title = models.CharField(max_length=50, verbose_name=_('title'))

    class Meta:
        db_table = 'images'
        verbose_name = _('image')
        verbose_name_plural = _('images')


class Properties(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('name'))
    value = models.CharField(max_length=250, verbose_name=_('value'))
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'props'
        verbose_name = _('property')
        verbose_name_plural = _('properties')


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('name'))
    published = models.BooleanField(verbose_name=_('published'), default=False)
    images = models.ManyToManyField(Image, verbose_name=_('images'))
    slug = models.SlugField(max_length=250, verbose_name=_('slug'), editable=False, unique=True)

    short_description = models.TextField(verbose_name=_('short description'), null=True, blank=True)
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('create date'))
    old_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    limited_edition = models.BooleanField(verbose_name=_('limited edition'), default=False)
    hot_offers = models.BooleanField(verbose_name=_('hot offers'), default=False)
    stock_balance = models.IntegerField(verbose_name=_('stock balance'), default=0)
    free_delivery = models.BooleanField(verbose_name=_('free delivery'), default=True)

    tags = models.ManyToManyField(Tags, verbose_name=_('tags'))
    views_count = models.IntegerField(verbose_name=_('views count'), default=0)

    class Meta:
        db_table = 'product'
        verbose_name = _('product')
        verbose_name_plural = _('products')
        indexes = [
            models.Index(fields=['name', 'slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_tags_str(self):
        return ' / '.join([tag.name for tag in self.tags.all()])

    @property
    def get_tags_link(self):
        catalog = reverse_lazy('catalog')
        return mark_safe(', '.join([f'<a href="{catalog}?tag={tag.name}">{tag.name}</a>' for tag in self.tags.all()]))


class Comment(models.Model):
    STATUS_CHOICES = [
        ('p', _('published')),
        ('d', _('deleted by admin'))
    ]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('author'), null=True)
    email = models.CharField(verbose_name=_('email'), max_length=50, null=True, blank=True)
    nickname = models.CharField(verbose_name=_('nickname'), max_length=50, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name=_('product'))
    text = models.TextField(verbose_name=_('text'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('create date'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p', verbose_name=_('status'))

    class Meta:
        db_table = 'comments'
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def short_comment(self):
        return f'{self.text[:15]}...' if len(self.text) > 15 else self.text

    short_comment.short_description = _('short description')

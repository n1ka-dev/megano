from django.db import models
from django.urls import reverse_lazy
from pytils.translit import slugify
from django.utils.translation import gettext_lazy as _


class BlogNews(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('title'))
    slug = models.SlugField(max_length=250, verbose_name=_('slug'), blank=True, unique=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('create date'))
    text = models.TextField(verbose_name=_('text'), null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_('is active'), default=False)
    image = models.FileField(upload_to='uploads/blog/')

    class Meta:
        db_table = 'blog'
        verbose_name = _('blog')
        verbose_name_plural = _('blog')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('post-detail',
                            kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    def short_descr(self):
        max_len = 150
        return f'{self.text[:max_len]}...' if len(self.text) > max_len+1 else self.text

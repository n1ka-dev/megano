from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    STATUS_CHOICES = [
        ('p', _('published')),
        ('d', _('deleted by admin'))
    ]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('author'), null=True)
    nickname = models.CharField(verbose_name='', max_length=50, null=True)
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

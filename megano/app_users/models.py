from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    avatar = models.FileField(blank=True, null=True, upload_to='uploads/avatars/')
    phone = models.CharField(max_length=12, blank=True, verbose_name=_('phone'))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))

    class Meta:
        db_table = 'profile'

from django.contrib import admin

from app_users.models import Profile


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['phone', 'get_email', 'user']

    def get_email(self, obj):
        return obj.user.email
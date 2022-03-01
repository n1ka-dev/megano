from django.contrib import admin

from app_blog.models import BlogNews


@admin.register(BlogNews)
class BlogNews(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active', 'short_descr']
    search_fields = ['title', 'text']



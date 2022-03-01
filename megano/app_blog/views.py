from django.shortcuts import render
from django.views.generic import ListView

from app_blog.models import BlogNews


class BlogView(ListView):
    model = BlogNews
    template_name = 'blog.html'
    context_object_name = 'blog_list'

    paginate_by = 12

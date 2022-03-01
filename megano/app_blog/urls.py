from django.urls import path

from app_blog.views import BlogView

urlpatterns = [
    path('', BlogView.as_view(), name='blog')
]
from django.urls import path

from app_blog.views import BlogView, PostDetailView

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('<slug>/', PostDetailView.as_view(), name='post-detail'),
]

from django.urls import path

from app_users.views import AuthUser

urlpatterns = [
    path('login/', AuthUser.as_view(), name='login'),
    path('register/', AuthUser.as_view(), name='register')
]

from django.urls import path

from app_users.views import SiteAuthUser, SiteRegistrationUserView

urlpatterns = [
    path('login/', SiteAuthUser.as_view(), name='login'),
    path('register/', SiteRegistrationUserView.as_view(), name='register')
]
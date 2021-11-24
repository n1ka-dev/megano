
from django.urls import path

from app_users.views import SiteAuthUser, SiteRegistrationUserView, ProfileUserView

urlpatterns = [
    path('login/', SiteAuthUser.as_view(), name='login'),
    path('register/', SiteRegistrationUserView.as_view(), name='register'),
    path('profile/', ProfileUserView.as_view(), name='profile')
]
from django.urls import path

from app_users.views import SiteAuthUser, SiteRegistrationUserView, ProfileUserView, SiteLogoutView, AccountUserView

urlpatterns = [
    path('login/', SiteAuthUser.as_view(), name='login'),
    path('logout/', SiteLogoutView.as_view(), name='logout'),
    path('register/', SiteRegistrationUserView.as_view(), name='register'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('account/', AccountUserView.as_view(), name='account'),
    path('history/', AccountUserView.as_view(), name='history')
]
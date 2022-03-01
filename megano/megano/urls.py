"""megano URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings


from .views import MainView
from django.urls import path, include

urlpatterns = [
                  path('', MainView.as_view(), name="main"),
                  path('__debug__/', include(debug_toolbar.urls)),
                  path('admin/', admin.site.urls),
                  path('catalog/', include('app_shop.urls')),
                  path('cart/', include('app_cart.urls')),
                  path('blog/', include('app_blog.urls')),
                  path('', include('app_users.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

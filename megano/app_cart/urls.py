from django.conf.urls import url
from django.urls import path

from app_cart import views
from app_cart.views import CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add')
]
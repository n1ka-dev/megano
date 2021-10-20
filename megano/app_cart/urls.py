from django.conf.urls import url
from django.urls import path

from app_cart import views
from app_cart.views import products_in_cart, cart_detail

urlpatterns = [
    path('', cart_detail, name='cart'),
    url(r'^update/(?P<product_id>\d+)/$', views.cart_update, name='cart_update'),
    path('products_in_cart/', products_in_cart, name='products_in_cart'),
]

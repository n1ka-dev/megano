from django.conf.urls import url
from django.urls import path

from app_cart.views import products_in_cart, cart_detail, cart_update, CheckoutView


urlpatterns = [
    path('', cart_detail, name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    url(r'^update/(?P<product_id>\d+)/$', cart_update, name='cart_update'),
    path('products_in_cart/', products_in_cart, name='products_in_cart'),
]

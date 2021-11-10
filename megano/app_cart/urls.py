from django.conf.urls import url
from django.urls import path

from app_cart.views import products_in_cart, cart_detail, cart_update, CheckoutView, save_order_info, PayView, \
    PayWaitView

urlpatterns = [
    path('', cart_detail, name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    url(r'^update/(?P<product_id>\d+)/$', cart_update, name='cart_update'),
    url(r'^save_order_info/$', save_order_info, name='save_order_info'),
    path('products_in_cart/', products_in_cart, name='products_in_cart'),
    path('pay/<uid>/', PayView.as_view(), name='pay'),
    path('pay/progress/<uid>/', PayWaitView.as_view(), name='pay-wait'),
]

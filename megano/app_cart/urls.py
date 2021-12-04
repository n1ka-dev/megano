from django.conf.urls import url
from django.urls import path

from app_cart.views import products_in_cart, cart_detail, cart_update, CheckoutView, save_order_info, PayView, \
    PayWaitView, get_status_order, OrderDetailView

urlpatterns = [
    path('', cart_detail, name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/<pk>', OrderDetailView.as_view(), name='order_detail'),
    url(r'^update/(?P<product_id>\d+)/$', cart_update, name='cart_update'),
    url(r'^save_order_info/$', save_order_info, name='save_order_info'),
    path('products_in_cart/', products_in_cart, name='products_in_cart'),
    path('pay/<uid>/', PayView.as_view(), name='pay'),
    path('pay/progress/<str:uid>/', PayWaitView.as_view(), name='pay-wait'),
    path('get-status/<uid>/', get_status_order, name='get_order_status'),
]

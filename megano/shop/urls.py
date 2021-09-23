from django.urls import path
from shop.views import CatalogView, ProductDetailView

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail')
]
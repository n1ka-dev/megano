from django.urls import path
from shop.views import CatalogView, ProductDetailView, CommentAdd

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    path('<slug:slug>/add_comment/', CommentAdd.as_view(), name='add-comment'),
]
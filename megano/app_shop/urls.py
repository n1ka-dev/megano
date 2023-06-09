from django.urls import path

from app_shop.views import CatalogView, ProductDetailView, CommentAdd, comments_list

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('<slug:category_slug>/', CatalogView.as_view(), name='category'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product-detail'),

    path('<slug:slug>/add_comment/', CommentAdd.as_view(), name='add-comment'),
    path('comments_product/<slug:slug>/', comments_list, name='comments_list'),
]
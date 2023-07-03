
from django.urls import path, include, re_path
from .views import AddToFavoriteView, FavoriteProductsListView, FavoriteProductDeleteView


urlpatterns = [
    path('add/<int:product_id>/', AddToFavoriteView.as_view(), name='add_to_favorite'),
    path('list/', FavoriteProductsListView.as_view(), name='list'),
    path('delete/<int:favorite_product_id>/', FavoriteProductDeleteView.as_view(), name='favorite_product_delete'),
]
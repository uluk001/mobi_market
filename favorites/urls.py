
from django.urls import path
from .views import FavoriteProductsListView, FavoriteProductsToggleView


urlpatterns = [
    path('list/', FavoriteProductsListView.as_view(), name='list'),
    path('toggle_favorite/<int:product_id>', FavoriteProductsToggleView.as_view(), name='toggle_favorite'),
]
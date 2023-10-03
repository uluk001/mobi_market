
from django.urls import path
from .views import FavoriteProductsListView, FavoriteProductsToggleView


urlpatterns = [
    path(
        'list/',
        FavoriteProductsListView.as_view(),
        name='list'),  # /favorite/list/
    path(
        'toggle_favorite/<int:product_id>',
        FavoriteProductsToggleView.as_view(),
        name='toggle_favorite'),  # /favorite/toggle_favorite/1
]

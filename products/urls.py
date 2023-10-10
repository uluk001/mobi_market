from django.urls import path
from .views import *


urlpatterns = [
    path('list/', 
        ProductListView.as_view()),
    # /products/list/
    path(
        'my_products_list/',
        MyProductsView.as_view()),
    # /products/my_products_list/
    path(
        'detail_product/<int:pk>',
        DetailProductView.as_view()),
    # /products/detail_product/1
    path(
        'create_product/',
        CreateProductView.as_view()),
    # /products/create_product/
    path(
        'update_product/<int:pk>',
        UpdateProductView.as_view()),
    # /products/update_product/1
    path(
        'delete_product/<int:pk>',
        DeleteProductView.as_view()),
    # /products/delete_product/1
    path(
        'my_products/',
        MyProductsView.as_view()),
    # /products/my_products/
    path(
        'create_additional_image/',
        CreateAdditionalImageView.as_view()),
    # /products/create_additional_image/
]

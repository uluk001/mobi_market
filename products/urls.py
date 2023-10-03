from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('list/', ProductListView.as_view()),
    path('my_products_list/', MyProductsView.as_view()),
    path('detail_product/<int:pk>', DetailProductView.as_view()),
    path('create_product/', CreateProductView.as_view()), # /products/create_product/
    path('update_product/<int:pk>', UpdateProductView.as_view()), # /products/update_product/1
    path('delete_product/<int:pk>', DeleteProductView.as_view()), # /products/delete_product/1
]

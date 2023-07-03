from django.urls import path, include, re_path
from .views import ProductListView, MyProductsView, DetailProductView, CreateProductView


urlpatterns = [
    path('list/', ProductListView.as_view()),
    path('my_products_list/', MyProductsView.as_view()),
    path('detail_product/<int:pk>', DetailProductView.as_view()),
    path('create_product/', CreateProductView.as_view()),
]
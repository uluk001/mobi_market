from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import FavoriteProductsSerializer
from products.models import Product
from products.serializers import ProductSerializer
from .models import FavoriteProducts


class FavoriteProductsToggleView(APIView):
    """
    Toggle favorite product.

    Use this endpoint to toggle favorite product.

    Parameters:
    - `product_id`: Id of the product

    Responses:
    201:
        description: Product added to favorites.
    200:
        description: Product removed from favorites.
    401:
        description: Unauthorized.
    """
    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        user = request.user

        try:
            favorite_product = FavoriteProducts.objects.get(
                product=product, user=user)
            favorite_product.delete()
            return Response(
                {"message": "Product removed from favorites"}, status=status.HTTP_200_OK)
        except FavoriteProducts.DoesNotExist:
            favorite_product = FavoriteProducts(product=product, user=user)
            favorite_product.save()
            return Response(
                {"message": "Product added to favorites"}, status=status.HTTP_201_CREATED)


class FavoriteProductsListView(APIView):
    """
    Get favorite products.

    Use this endpoint to get favorite products.

    Responses:
    200:
        description: A list of favorite products.
    401:
        description: Unauthorized.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorite_products = FavoriteProducts.objects.filter(user=request.user)
        serializer = FavoriteProductsSerializer(favorite_products, many=True)
        favorite_products_data = serializer.data

        for favorite_product in favorite_products_data:
            product = Product.objects.get(id=favorite_product['product'])
            product_serializer = ProductSerializer(product)
            favorite_product['product'] = product_serializer.data

        return Response(favorite_products_data, status=status.HTTP_200_OK)

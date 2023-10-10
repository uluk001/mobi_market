from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import FavoriteProductsSerializer
from products.models import Product
from .models import FavoriteProducts
from products.serializers import ProductCreateSerializer
from accounts.models import CustomUser
from drf_yasg.utils import swagger_auto_schema


class FavoriteProductsToggleView(APIView):

    @swagger_auto_schema(
        operation_description="Toggle favorite product.",
        responses={
            201: '{"message": "Product added to favorites"}',
            200: '{"message": "Product removed from favorites"}',
            403: "Forbidden. The user does not have the required permissions.",
            404: "Product or user not found."
        }
    )
    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        favorite_product, created = FavoriteProducts.objects.get_or_create(product=product, user=user)
        
        if created:
            return Response(
                {"message": "Product added to favorites"}, status=status.HTTP_201_CREATED)
        else:
            favorite_product.delete()
            return Response(
                {"message": "Product removed from favorites"}, status=status.HTTP_200_OK)

    permission_classes = [IsAuthenticated]


class FavoriteProductsListView(APIView):

    @swagger_auto_schema(
        operation_description="List all favorite products.",
        responses={
            200: FavoriteProductsSerializer,
            403: "Forbidden. The user does not have the required permissions.",
            404: "User not found.",
        }
    )
    def get(self, request):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        favorite_products = FavoriteProducts.objects.filter(user=user)
        serializer = FavoriteProductsSerializer(favorite_products, many=True)
        favorite_products_data = serializer.data

        favorite_products_dict = []
        for favorite_product_data in favorite_products_data:
            product_id = favorite_product_data['product']
            product = Product.objects.get(pk=product_id)
            product_serializer = ProductCreateSerializer(product)
            product_data = product_serializer.data
            favorite_products_dict.append(product_data)
        return Response(favorite_products_dict, status=status.HTTP_200_OK)

    permission_classes = [IsAuthenticated]

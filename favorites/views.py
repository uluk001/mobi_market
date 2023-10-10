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
            200: "Product removed from favorites.",
            201: "Product added to favorites.",
            403: "Forbidden. The user does not have the required permissions.",
        }
    )

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            print(user)
            print(request.user.id)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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

    @swagger_auto_schema(
        operation_description="List all favorite products.",
        responses={
            200: "List of favorite products.",
            403: "Forbidden. The user does not have the required permissions.",
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = CustomUser.objects.get(pk=request.user.id)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        favorite_products = FavoriteProducts.objects.filter(user=user)
        serializer = FavoriteProductsSerializer(favorite_products, many=True)
        favorite_products_data = serializer.data

        favorite_products = {}
        for favorite_product_data in favorite_products_data:
            product_id = favorite_product_data['product']
            product = Product.objects.get(pk=product_id)
            product_serializer = ProductCreateSerializer(product)
            favorite_products[product_id] = product_serializer.data

        return Response(favorite_products, status=status.HTTP_200_OK)

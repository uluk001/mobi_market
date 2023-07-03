from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import FavoriteProductsSerializer
from products.models import Product
from products.serializers import ProductSerializer
from .models import FavoriteProducts

class AddToFavoriteView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'product': product_id,
        }
        serializer = FavoriteProductsSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response("Product added to favorites", status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FavoriteProductsListView(APIView):
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



class FavoriteProductDeleteView(APIView):
    def delete(self, request, favorite_product_id):
        try:
            favorite_product = FavoriteProducts.objects.get(id=favorite_product_id, user=request.user)
        except FavoriteProducts.DoesNotExist:
            return Response({'error': 'Favorite product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        favorite_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
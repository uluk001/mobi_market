from django.db.models import Count
from .serializers import *
from rest_framework import generics, status
from .models import Product
from accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ProductListView(generics.ListAPIView):
    """
    List all products.

    Use this endpoint to list all products.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.annotate(
            like_count=Count(
                'favoriteproducts__user',
                distinct=True))
        return queryset


class MyProductsView(generics.ListAPIView):
    """
    List my products.

    Use this endpoint to list all products of the current user.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(owner=user)
        return queryset


class DetailProductView(generics.RetrieveAPIView):
    """
    Retrieve a product.

    Use this endpoint to retrieve a product.

    Parameters:
    - `pk`: Id of the product
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CreateProductView(APIView):
    """
    Create a new product.

    Use this endpoint to create a new product.

    Parameters:
    - `title`: Title of the product
    - `description`: Description of the product
    - 'more_info': More info about the product
    - `price`: Price of the product
    - `image`: Image of the product 
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        owner = request.user
        data = request.data
        data['owner'] = owner.id
        product_serializer = ProductCreateSerializer(data=data)
        if product_serializer.is_valid():
            product_serializer.save(owner=request.user)
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



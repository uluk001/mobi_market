from django.db.models import Count
from .serializers import *
from rest_framework import generics, status
from .models import Product
from accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProductListView(generics.ListAPIView):

    @swagger_auto_schema(
        operation_description="List all products.",
        responses={
            200: ProductSerializer,
            403: "Forbidden. The user does not have the required permissions.",
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.annotate(
            like_count=Count(
                'favoriteproducts__user',
                distinct=True))
        return queryset


class MyProductsView(generics.ListAPIView):

    @swagger_auto_schema(
        operation_description="List all products of the user.",
        responses={
            200: ProductSerializer,
            403: "Forbidden. The user does not have the required permissions.",
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(owner=user).annotate(
            like_count=Count(
                'favoriteproducts__user',
                distinct=True))
        return queryset


class DetailProductView(generics.RetrieveAPIView):
    @swagger_auto_schema(
        operation_description="Detail of a product.",
        responses={
            200: ProductDetailSerializer,
            403: "Forbidden. The user does not have the required permissions.",
            404: "Product not found."
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


class CreateAdditionalImageView(generics.CreateAPIView):
    
        @swagger_auto_schema(
            operation_description="Create an additional image.",
            manual_parameters=[
                openapi.Parameter('image', openapi.IN_QUERY, description="Image of the product", type=openapi.TYPE_FILE),
                openapi.Parameter('product', openapi.IN_QUERY, description="Product", type=openapi.TYPE_INTEGER),
            ],
            responses={
                201: ProductDetailSerializer,
                400: "Bad request. The request was invalid.",
                403: "Forbidden. The user does not have the required permissions.",
            }
        )
        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)
    
        parser_classes = (MultiPartParser, FormParser)
        serializer_class = AdditionalImageSerializer
        permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class CreateProductView(APIView):

    @swagger_auto_schema(
        operation_description="Create a product.",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_FORM, description="Title of the product", type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_FORM, description="Description of the product", type=openapi.TYPE_STRING),
            openapi.Parameter('more_info', openapi.IN_FORM, description="More info about the product", type=openapi.TYPE_STRING),
            openapi.Parameter('price', openapi.IN_FORM, description="Price of the product", type=openapi.TYPE_INTEGER),
            openapi.Parameter('image', openapi.IN_FORM, description="Image of the product", type=openapi.TYPE_FILE),
        ],
        responses={
            201: ProductCreateSerializer(),
            400: "Bad request. The request was invalid.",
            403: "Forbidden. The user does not have the required permissions.",
        }
    )
    def post(self, request, *args, **kwargs):
        owner = request.user
        data = request.data.copy()
        data['owner'] = owner.id
        product_serializer = ProductCreateSerializer(data=data)
        if product_serializer.is_valid():
            product_serializer.save(owner=request.user)
            return Response(
                product_serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                product_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]



class UpdateProductView(generics.UpdateAPIView):
    serializer_class = ProductUpdateSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Update a product.",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="Title of the product", type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_QUERY, description="Description of the product", type=openapi.TYPE_STRING),
            openapi.Parameter('more_info', openapi.IN_QUERY, description="More info about the product", type=openapi.TYPE_STRING),
            openapi.Parameter('price', openapi.IN_QUERY, description="Price of the product", type=openapi.TYPE_INTEGER),
            openapi.Parameter('image', openapi.IN_QUERY, description="Image of the product", type=openapi.TYPE_FILE),
        ],
        responses={
            200: "Product updated successfully.",
            403: "Forbidden. The user does not have the required permissions.",
            404: "Product not found."
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteProductView(generics.DestroyAPIView):

    @swagger_auto_schema(
        operation_description="Delete a product.",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="Id of the product", type=openapi.TYPE_INTEGER),
        ],
        responses={
            204: "Product deleted successfully.",
            403: "Forbidden. The user does not have the required permissions.",
            404: "Product not found."
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

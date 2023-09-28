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
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.annotate(like_count=Count('favoriteproducts__user', distinct=True))
        return queryset

class MyProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(owner=user)
        return queryset
    
class DetailProductView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CreateProductView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticated]


    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({'reply': 'Product added'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

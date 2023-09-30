from rest_framework import serializers
from .models import FavoriteProducts


class FavoriteProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProducts
        fields = '__all__'

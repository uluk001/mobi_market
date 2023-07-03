from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'owner']

    def get_owner(self, obj):
        if 'request' in self.context:
            return self.context['request'].user
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['owner'] = request.user
        return super().create(validated_data)
from rest_framework import serializers
from accounts.models import User
from .models import FavoriteProducts

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FavoriteProductsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    id = serializers.IntegerField(source='pk')

    class Meta:
        model = FavoriteProducts
        fields = ['id', 'product', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)

    def get_user(self, obj):
        if 'request' in self.context:
            return self.context['request'].user
        return None

        


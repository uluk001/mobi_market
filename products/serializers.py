from rest_framework import serializers
from .models import Product, AdditionalImage
from accounts.serializers import CustomUserSerializer


class ProductSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer()
    like_count = serializers.IntegerField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_owner(self, obj):
        if 'request' in self.context:
            return self.context['request'].user
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['owner'] = request.user
        return super().create(validated_data)


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['owner', 'like_count']


class AdditionalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalImage
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    additional_images = AdditionalImageSerializer(source='additionalimage_set', many=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['owner', 'like_count']
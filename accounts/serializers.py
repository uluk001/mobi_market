from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = 'accounts_user'  # Установите уникальное значение ref_name для сериализатора accounts
        fields = ['id', 'username', 'email', 'phone_number', 'is_verified_phone_number']
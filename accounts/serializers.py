from rest_framework import serializers
from accounts.models import User, EmailVerification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = 'accounts_user'
        fields = ['id', 'username', 'email',]

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ['code', ]

    
    def get_user(self, obj):
        if 'request' in self.context:
            return self.context['request'].user
        return None
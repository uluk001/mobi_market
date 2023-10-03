from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True)  # Добавлено поле username
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароль не совпадает, попробуйте еще раз'})
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']  # Получаем username из валидированных данных
        password = validated_data['password']
        user = User.objects.create_user(email=email, username=username, password=password)  # Создаем пользователя с username
        user.is_active = False
        user.token_auth = get_random_string(64)
        user.save()

        refresh = RefreshToken.for_user(user)  # Сохраняем токен в поле auth_token

        current_site = get_current_site(self.context['request'])
        domain = current_site.domain
        protocol = 'https' if self.context['request'].is_secure() else 'http'
        confirmation_link = reverse('confirm_email', kwargs={'token': user.token_auth})

        subject = 'Подтверждение регистрации'
        message = f'Подтвердите вашу регистрацию по ссылке: \n\n{protocol}://{domain}{confirmation_link}'
        from_email = 'azatss442@gmail.com'
        to_email = email
        send_mail(subject, message, from_email, [to_email], fail_silently=False)

        return user


class ConfirmPhoneNumberSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from .serializers import CustomUserSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

class UserProfileViewSet(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Создаем JWT-токен
        refresh = RefreshToken.for_user(user)
        user.auth_token = str(refresh.access_token)  # Сохраняем токен в поле auth_token

        # Отправляем письмо для подтверждения регистрации (как в вашем коде)

        # Возвращаем информацию о пользователе и токене в ответе
        response_data = {
            'username': user.username,
            'email': user.email,
            'token': user.auth_token
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class ConfirmEmailView(generics.GenericAPIView):
    @staticmethod
    def get(request, token):
        try:
            user = User.objects.get(token_auth=token)  # Используем поле 'token_auth' как ранее
            if user.is_active:
                print('User is already activated')  # Отладочное сообщение
                return Response({'detail': 'User is already activated'}, status=status.HTTP_200_OK)

            user.is_active = True
            user.save()

            login(request, user)
            refresh = RefreshToken.for_user(user)
            print('Email confirmation successful')  # Отладочное сообщение

            # Выполним редирект на указанный URL после успешной активации
            return redirect('https://neobis-front-marketplace-tau.vercel.app/')  # Замените URL на нужный

        except User.DoesNotExist:
            print('Invalid token')  # Отладочное сообщение
            return Response({'detail': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
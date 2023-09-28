from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *


urlpatterns = [
    path('profile/', UserProfileViewSet.as_view()),
    path('confirm_email/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('', TokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
]
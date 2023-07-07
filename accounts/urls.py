
from django.urls import path
from .views import SendVerificationCodeToEmailView, EmailVerificationView


urlpatterns = [
    path('send_verification_code_to_email/', SendVerificationCodeToEmailView.as_view(), name='send_verification_code_to_email'),
    path('email_verification/<str:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import EmailVerificationSerializer
from .models import User, EmailVerification
import datetime, uuid, string, random
from django.utils.timezone import now
from django.shortcuts import get_object_or_404


class SendVerificationCodeToEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        code = ''.join(random.choices(string.octdigits, k=4))

        user = User.objects.get(id=user_id)
        expiration = now() + datetime.timedelta(hours=48)
        record = EmailVerification.objects.create(code=code, user=user, expiration=expiration)
        record.send_verification_email()
        return Response({"message": "We have sent a 4 digit code to your email"}, status=status.HTTP_200_OK)




        # user_id = request.user.id
        # code = ''.join(random.choices(string.octdigits, k=4))

        # user = User.objects.get(id=user_id)
        # expiration = now() + datetime.timedelta(hours=48)
        # record = EmailVerification.objects.create(code=code, user=user, expiration=expiration)
        # record.send_verification_email()
        # return Response({"message": "We have sent a 4 digit code to your email"}, status=status.HTTP_200_OK)


class EmailVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        email = request.user.email
        user = get_object_or_404(User, email=email)
        email_verification = EmailVerification.objects.filter(user=user, code=code)

        print(f'--------------------{email}----{code}-----------------')
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return Response('Электронная почта подтверждена')
        else:
            return Response('Попробуйте заново')

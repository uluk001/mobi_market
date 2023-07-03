from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    phone_number = models.CharField(max_length=255, unique=True)
    is_verified_phone_number = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['phone_number', 'email',]

# class PhoneNumberVerification(models.Model):
#     code = models.UUIDField(unique=True)
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     expiration = models.DateTimeField()

#     def __str__(self):
#         return f'EmailVerification object for {self.user.email}'

    # def send_verification_email(self):
    #     link = f'users/verify/{self.user.email}/{self.code}'
    #     verification_link = f'{settings.DOMAIN_NAME}{link}'
    #     subject = f'Подтверждение учетной записи для {self.user.username}'
    #     message = f'Для подтверждение учетной записи перейдите по ссылке {verification_link}'
    #     send_mail(
    #         subject=subject,
    #         message=message,
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[self.user.email],
    #         fail_silently=False
    #     )

    # def is_expired(self):
    #     return True if now() >= self.expiration else False
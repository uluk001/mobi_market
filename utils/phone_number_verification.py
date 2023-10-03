from twilio.rest import Client
import random
from django.conf import settings
from django.utils import timezone
from accounts.models import PhoneNumberVerification
from accounts.models import CustomUser


def send_phone_number_verification(user_id):
    user = CustomUser.objects.get(id=user_id)
    code = generate_code()
    expiration = timezone.now() + timezone.timedelta(minutes=10)
    verification = PhoneNumberVerification.objects.create(
        code=code,


        user=user,
        expiration=expiration
    )
    send_verification_phone_number(code, user.phone_number)
    return verification


def send_verification_phone_number(code, phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=f'+996{phone_number}',
        from_=settings.TWILIO_PHONE_NUMBER,
        body=f'Ваш код: {code}')
    return message.sid


def generate_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])

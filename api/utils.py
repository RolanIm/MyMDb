from django.core.mail import send_mail
from MyMDb.settings import EMAIL_HOST_USER


def send_email(data):
    message = (f'Dear {data.get("username")},\n'
               f'Here are your confirmation code: '
               f'{data.get("confirmation_code")}')
    send_mail(
        subject='Please, confirm your email.',
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[data.get("email")],
        fail_silently=False
    )

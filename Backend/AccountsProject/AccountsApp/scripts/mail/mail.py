from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
import logging


class Email:

    @staticmethod
    def send_mail(email, subject, message, html_message):
        try:

            send_mail(
                subject=subject,
                message=message,
                html_message=html_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        except BadHeaderError:
            logging.warning('BadHeaderError')

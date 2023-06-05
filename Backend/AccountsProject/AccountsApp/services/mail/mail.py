import traceback
from pathlib import Path

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, EmailMessage, EmailMultiAlternatives
import logging


class Mail:

    def send_mail(self, email_list, subject=None, message=None, html_message=None, filename=None):
        try:
            # self.mail.message()
            mail = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.EMAIL_HOST_USER,
                to=email_list,
            )
            mail.attach_alternative(html_message, "text/html")
            # open('test_txt.txt', 'w')
            logging.warning('blabla')

            # mail.content_subtype='html'
            logging.warning(filename)

            if filename:
                logging.warning('->|12344|<-')
                mail.attach_file(filename)
            mail.send()
            # send_mail(
            #     subject=subject,
            #     message=message,
            #     html_message=html_message,
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[email],
            #     fail_silently=False,
            # )

        except BadHeaderError:
            logging.warning('BadHeaderError')


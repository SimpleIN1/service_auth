import os

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from AccountsApp.services.token.jwt_token import Jwt
from AccountsApp.services.mail.mail_send import EmailVerify, InfoCreatedProfile, RegisteredProfile, \
    SuccessOpeningAccessClient
from AccountsApp.services.token.mail_token import create_token
from AccountsApp.services.user_view import send_email_directors

User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save(created, **kwargs):
    instance = kwargs['instance']

    if not instance.is_added_admin_panel \
            and created \
            and not instance.is_verify: # False and

        #Отправка письма пользователю
        RegisteredProfile(email=[instance.email], context={
            'protocol': settings.PROTOCOL,
            'site_name': settings.HOST,
        }).send()
        # print('==')
        # print(instance.file._file)
        # print('==')
        # print('***(--')
        # print(os.listdir('media/files/gorgh31/'))
        # print('***(--')
        send_email_directors(instance)
        # send_email_to_directors.delay(directors, instance)
        # print('***(')
        # print(os.listdir('media/files/gorgh31/'))
        # print('***(')

# @receiver(pre_save, sender=User)
# def user_model_pre_save(sender, instance, *args, **kwargs):
#     if instance.is_verify and instance.is_active and not instance.is_email_getted:
#
#         password = secrets.token_urlsafe(11)
#         instance.set_password(password)
#
#         instance.is_verify = True
#         instance.is_email_getted = True
#         SuccessOpeningAccessClient(
#             email=[instance.email],
#             context={
#                 'protocol': settings.PROTOCOL,
#                 'site_name': settings.HOST,
#                 'port': settings.PORT,
#                 'email': instance.email,
#                 'password': password,
#             }
#         ).send()

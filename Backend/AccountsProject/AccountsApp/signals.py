from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from AccountsApp.services.token.jwt_token import Jwt
from AccountsApp.services.mail.mail_send import EmailVerify, InfoCreatedProfile, RegisteredProfile, \
    SuccessOpeningAccessClient
from AccountsApp.services.token.mail_token import create_token
from AccountsApp.services.user_view import filter_user_model

import secrets


User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save(created, **kwargs):
    instance = kwargs['instance']

    if created and not instance.is_verify: # False and

        email = instance.email
        token = create_token(instance, is_password=True)#instance.id,email, uuid, settings.SECRET_KEY) #Jwt.create_tmp_access_token(email)

        #Отправка письма пользователю
        RegisteredProfile(email=[email], context={
            'protocol': settings.PROTOCOL,
            'site_name': settings.HOST,
        }).send()
        print(email, 'письмо отправлено')
        emails = filter_user_model(type_user=1, is_getter_email=True)
        if emails:
            # Отправка письма директору
            InfoCreatedProfile(email=[emails], context={
                'protocol': settings.PROTOCOL,
                'site_name': settings.HOST,
                'port': settings.PORT,
                'last_name': instance.last_name,
                'first_name': instance.first_name,
                'middle_name': instance.middle_name,
                'email': email,
                'org_name': instance.organization_name,
                # 'url': f'api/auth/access_client/?email={email}&'
                #        f'token={token}',
            }).send(instance.file.name) #{settings.URL_PAGE["reset_password"]}


@receiver(pre_save, sender=User)
def user_model_pre_save(sender, instance, *args, **kwargs):

    if not instance.is_verify and instance.is_active:

        password = secrets.token_urlsafe(11)
        instance.set_password(password)

        instance.is_verify = True
        SuccessOpeningAccessClient(
            email=[instance.email],
            context={
                'protocol': settings.PROTOCOL,
                'site_name': settings.HOST,
                'port': settings.PORT,
                'email': instance.email,
                'password': password,
            }
        ).send()

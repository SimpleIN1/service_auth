from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from AccountsApp.scripts.token.jwt_token import Jwt
from AccountsApp.scripts.mail.mail_send import EmailVerify
from AccountsApp.scripts.token.mail_token import create_token

User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save(created, **kwargs):
    instance = kwargs['instance']

    if created and not instance.is_verify:

        email = instance.email
        token = create_token(instance, is_password=True)#instance.id,email, uuid, settings.SECRET_KEY) #Jwt.create_tmp_access_token(email)

        EmailVerify(email=email, context={
            'protocol': settings.PROTOCOL,
            'site_name': settings.HOST,
            'url': f'{settings.URL_PAGE["email_verify"]}?email={email}&'
                   f'token={token}&'
                   f'uuid={instance.uuid}',
        }).send()





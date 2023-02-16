from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.urls import reverse

from .scripts.jwt_token import Jwt
from .scripts.mail_send import EmailVerify
from .tasks import send_email


User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save(created, **kwargs):
    instance = kwargs['instance']

    if created and not instance.is_verify:
        # html_message = render_to_string('AccountsApp/verify_email.html', context={
        #     'protocol': 'https',
        #     'site_name': 'fire-activity-map.com',
        #     'url': 'url',
        # })
        #
        # send_email.delay(
        #     email=instance.email,
        #     subject='Verify email on fire-activity-map.com',
        #     html_message=html_message
        # )
        email = instance.email
        token = Jwt.create_tmp_access_token(email)

        EmailVerify(email=email, context={
            'protocol': settings.PROTOCOL,
            'site_name': settings.HOST,
            'url': f'{settings.URL_PAGE["email_verify"]}?email={email}&'
                   f'token={token}&'
                   f'uuid={instance.uuid}',
        }).send()





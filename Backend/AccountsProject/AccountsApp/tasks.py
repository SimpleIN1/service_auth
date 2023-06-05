import logging
import traceback

from django.conf import settings


from AccountsApp.services.token.mail_token import create_token
from celery_app.celery_app import app
from AccountsApp.services.mail.mail import Mail


@app.task()
def send_email(email, subject, message='', html_message='', filename=None):
    try:
        mail = Mail()
        mail.send_mail(email, subject, message, html_message, filename)
    except Exception as er:
        # logging.warning(traceback.format_exc())
        logging.warning(f'Task of the faction send_mail call error: {er}')


@app.task()
def send_email_to_directors(directors, instance):
    from AccountsApp.services.mail.mail_send import InfoCreatedProfile
    try:
        # print('--'*12)
        # print(1234)
        # print('--'*12)
        for director in directors:
            token = create_token(director, is_password=True)
            InfoCreatedProfile(email=[director.email], context={
                'protocol': settings.PROTOCOL,
                'site_name': settings.HOST,
                'port': settings.PORT,
                'last_name': instance.last_name,
                'first_name': instance.first_name,
                'middle_name': instance.middle_name,
                'email': instance.email,
                'org_name': instance.organization_name,
                'url': f'{settings.URL_PAGE["url_for_access_client"]}?email={director.email}&'
                       f'token={token}&uuid={director.uuid}',
            }).send(instance.file.name)
    except Exception as er:
        logging.warning(f'Task of the faction send_mail call error: {er}')


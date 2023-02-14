import logging

from celery_app.celery_app import app
from AccountsApp.scripts.mail import Email


@app.task()
def send_email(email, subject, message='', html_message=''):
    try:
        Email.send_mail(email, subject, message, html_message)
    except Exception as er:
        logging.warning(f'Task of the faction send_mail call error: {er}')

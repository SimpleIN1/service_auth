import logging

from celery_app.celery_app import app
from AccountsApp.services.mail.mail import Mail


@app.task()
def send_email(email, subject, message='', html_message='', filename=None):
    try:
        mail = Mail()
        mail.send_mail(email, subject, message, html_message, filename)
    except Exception as er:
        logging.warning(f'Task of the faction send_mail call error: {er}')

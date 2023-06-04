from django.template.loader import render_to_string
from django.conf import settings

from AccountsApp.tasks import send_email


class EmailSend:
    template = None
    context = None
    subject = None
    email = None

    def __init__(self, email, context, ):
        self.context = context
        self.email = email

    def send(self, filename=None):
        # self.context['subject'] = self.subject
        html_message = render_to_string(self.template, context=self.context)
        send_email.delay(
            email=self.email,
            subject=self.subject,
            html_message=html_message,
            filename=filename
        )


class EmailResetPassword(EmailSend):
    template = 'AccountsApp/reset_password.html'
    subject = 'Сброс пароля на сайте %s' % settings.HOST


class EmailVerify(EmailSend):
    template = 'AccountsApp/verify_email.html'
    subject = 'Поддтверждение на сайте %s' % settings.HOST


class RecoveryAccount(EmailSend):
    template = 'AccountsApp/recovery_account.html'
    subject = 'Восстановление учетной записи на сайте %s' % settings.HOST


class InfoCreatedProfile(EmailSend):
    template = 'AccountsApp/info_created_profile.html'
    subject = 'Пользователь произвел регистрацию на %s' % settings.HOST


class RegisteredProfile(EmailSend):
    template = 'AccountsApp/registered_profile.html'
    subject = 'Регистрация на %s' % settings.HOST


class SuccessOpeningAccessClient(EmailSend):
    template = 'AccountsApp/success_opening_access_client.html'
    subject = 'Получен доступ к %s' % settings.HOST


class LoginDetails(EmailSend):
    template = 'AccountsApp/login_details.html'
    subject = 'Данные для входа на %s' % settings.HOST
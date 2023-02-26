from django.template.loader import render_to_string

from AccountsApp.tasks import send_email


class EmailSend:
    template = None
    context = None
    subject = None
    email = None

    def __init__(self, email, context):
        self.context = context
        self.email = email

    def send(self):
        html_message = render_to_string(self.template, context=self.context)
        send_email.delay(
            email=self.email,
            subject=self.subject,
            html_message=html_message
        )


class EmailResetPassword(EmailSend):
    template = 'AccountsApp/reset_password.html'
    subject = 'Сброс пароля на сайте fire-activity-map.com'


class EmailVerify(EmailSend):
    template = 'AccountsApp/verify_email.html'
    subject = 'Поддтверждение на сайте fire-activity-map.com'


class RecoveryAccount(EmailSend):
    template = 'AccountsApp/recovery_account.html'
    subject = 'Восстановление учетной записи на сайте fire-activity-map.com'

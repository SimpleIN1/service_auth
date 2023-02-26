from django.apps import AppConfig


class AccountsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AccountsApp'
    verbose_name = 'Приложение для учетных записей'

    def ready(self):
        from . import signals

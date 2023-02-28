from django.core.management import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from os import getenv


class Command(BaseCommand):
    help = 'This command create superuser'
    user_model = get_user_model()

    def __get_admin_data(self):
        load_dotenv()

        username = getenv('USERNAME_ADMIN', 'admin')
        email = getenv('EMAIL_ADMIN', 'admin@admin.com')
        password = getenv('PASSWORD_ADMIN', 'admin')

        if not(username and email and password):
            raise CommandError('the fields username, email, password is required. You '
                               'must define all these fields in the .env file')

        if self.user_model.objects.filter(
            email=email, is_staff=True
        ).exists():
            raise CommandError('superuser is already exists with this email')

        return username, email, password

    def handle(self, *args, **options):
        username, email, password = self.__get_admin_data()

        superuser = self.user_model(
            username=username,
            email=email,
        )
        superuser.set_password(password)
        superuser.is_staff = True
        superuser.is_active = True
        superuser.is_verify = True
        superuser.is_superuser = True
        superuser.save()

        self.stdout.write('Superuser is created. ' + self.style.SUCCESS('OK'))

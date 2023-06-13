import traceback
from datetime import datetime

from django.contrib.auth import password_validation
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.conf import settings
import uuid
from mimetypes import MimeTypes


def upload_to(inst, fn):
    try:
        dirname = str(inst.email).split('@')[0]
        expansion = settings.CONTENT_TYPE[inst.file._file.content_type]
        filename = f'{inst.last_name}_{inst.first_name}_{inst.middle_name}.{expansion}'
        # print('FFF')
        return f'files/{dirname}/{filename}'
    except Exception as e:
        print(traceback.format_exc())


class User(AbstractUser):
    '''# Переопределенная модель user с добавленными параметрами:
     middle_name, organization_name, uuid, is_verify, is_reset_password #'''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(
        _("email address"),
        unique=True
    )
    username = models.CharField(
        max_length=150,
        default='',
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    middle_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Отчество',
        help_text=_(
            'Если имеется.'
        ),
    )
    organization_name = models.CharField(
        max_length=400,
        verbose_name='Наименование организации'
    )
    send_email_to_director = models.BooleanField(
        default=False,
    )
    is_email_getted = models.BooleanField(
        default=False,
        verbose_name='Отправлено письмо с паролем'
    )
    is_open_app = models.BooleanField(
        default=False,
    )

    is_added_admin_panel = models.BooleanField(
        default=False
    )

    is_verify = models.BooleanField(
        default=False,
        verbose_name='Подтвержденная почта.'
    )
    TYPE_USER = (
        (1, 'Директор'),
        (2, 'Обычный рядовой пользователь'),
    )
    type_user = models.SmallIntegerField(
        verbose_name='Тип пользователя',
        choices=TYPE_USER,
        default=2,
    )
    is_getter_email = models.BooleanField(
        verbose_name='Является получателем писем для проверки документов',
        default=False,
        help_text=_('При каждом добавлении пользователя, директор будет получать письмо с данными о пользователе.')
    )
    uuid = models.UUIDField(default=uuid.uuid4(), db_index=True)
    is_reset_password = models.BooleanField(default=False)
    file = models.FileField(
        verbose_name='Файл(ы) для получения доступа',
        upload_to=lambda inst, fn: upload_to(inst, fn),
        blank=True,
        null=True,
        default='',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'odt', 'docx', 'doc']
            )
        ],
        help_text=_(f'Поддерживаемые форматы: {", ".join(["pdf", "odt", "docx", "doc"])}'),
    )

    def update_last_login(self):
        self.last_login = datetime.now()

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'



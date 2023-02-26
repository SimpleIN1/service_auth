from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid


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
    is_verify = models.BooleanField(
        default=False,
        verbose_name='Подтвержденная почта.'
    )
    uuid = models.UUIDField(default=uuid.uuid4(), db_index=True)
    is_reset_password = models.BooleanField(default=False)

    # is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

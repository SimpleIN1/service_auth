from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid


class User(AbstractUser):
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
    )
    first_name = models.CharField(
        max_length=150,
    )
    middle_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    organization_name = models.CharField(
        max_length=400,
    )
    uuid = models.UUIDField(default=uuid.uuid4(), db_index=True)
    is_verify = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    is_reset_password = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_user'

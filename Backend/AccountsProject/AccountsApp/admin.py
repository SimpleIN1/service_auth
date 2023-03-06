from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


User = get_user_model()


@admin.register(User)
class UserModelAdmin(UserAdmin):
    # pass
    # exclude = [
    #     'uuid',
    #     'is_reset_password',
    #     'username',
    # ]
    list_display = [
        'id',
        'email',
        'last_name',
        'first_name',
        'middle_name',
        'organization_name',
        'is_active',
        'is_verify',
        'is_staff',
        'is_superuser',
    ]
    list_filter = [
        'is_active',
        'is_verify',
        'is_staff',
        'is_superuser',
    ]
    search_fields = [
        'id',
        'email',
        'last_name',
        'first_name',
        'middle_name',
        'organization_name',
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "last_name",
                    "first_name",
                    "middle_name",
                    "organization_name",
                    "password1",
                    "password2"
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("password", )}), #"username",
        (_("Personal info"), {
            "fields":
                (
                    "last_name",
                    "first_name",
                    "middle_name",
                    "organization_name",
                    "email",
                    "is_verify",
                )
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
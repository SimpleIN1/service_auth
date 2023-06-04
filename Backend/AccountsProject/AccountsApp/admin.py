from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from AccountsApp.forms import UserPasswordNorRequiredCreationForm

# from AccountsApp.models import FileModel

User = get_user_model()


@admin.register(User)
class UserModelAdmin(UserAdmin):

    list_display = [
        'id',
        'email',
        # 'uuid',
        'last_name',
        'first_name',
        'middle_name',
        'organization_name',
        'is_active',
        'is_verify',
        'is_staff',
        'is_superuser',
        'type_user',
        'is_getter_email',
    ]
    list_filter = [
        'is_active',
        'is_verify',
        'is_staff',
        'is_superuser',
        'is_getter_email',
        'type_user',
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
                    "type_user",
                    "is_getter_email",
                    "select_action_password",

                    "send_gen_password",
                    "password1",
                    "password2",
                    "send_password",
                    "send_email_to_director",
                    "open_access",
                    'file',
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
                    "type_user",
                    "is_getter_email",
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
                    'file',
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    exclude = ('is_email_getted', )

    add_form = UserPasswordNorRequiredCreationForm

    class Media:
        js = ('AccountsApp/js/base-admin.js', )

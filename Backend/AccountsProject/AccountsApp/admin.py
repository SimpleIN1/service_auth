from django.contrib import admin

from .models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    exclude = [
        'uuid',
        'is_reset_password',
        'username',
    ]
    list_display = [
        'id',
        'email',
        'last_name',
        'first_name',
        'middle_name',
        'organization_name',
        'is_active',
        'is_verify',
    ]
    list_filter = [
        'is_active',
        'is_verify',
    ]
    search_fields = [
        'id',
        'email',
        'last_name',
        'first_name',
        'middle_name',
        'organization_name',
    ]

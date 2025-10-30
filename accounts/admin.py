from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "email",
        "is_staff",
        "is_active"
    ]
    list_filter = [
        "is_staff",
        "is_active"
    ]
    search_fields = ["email", "username"]
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "last_name",
                "first_name",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "groups",
                "user_permissions",
                "is_superuser",
            ),
        },
    ),
)


admin.site.register(CustomUser, CustomUserAdmin)

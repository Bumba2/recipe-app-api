from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
"""=> _ this is the recommended convention for converting
strings to human readable text in python.
We do this so it gets passed through the translation
engine (which would make translation easier)"""
from core import models

"""Create custom user admin
=>order the user by id and show email and name"""


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name"]
    """define the sections for the field sets in
            our change and create page."""
    """each Bracket is a section"""
    """1. bit: Title for the section, 2. bit: permissions,
    3. bit: date Section"""
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name", )}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")}
        ),
        (_("Important dates"), {"fields": ("last_login", )})
    )
    """If we ever want to add extra fields to our user model,
    e. g. "lost logout" we can add this quite easily."""
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2")
        }),
    )
    """1 field: Title of the section (here None),
    2: classes (standard is wide),
    3: fields. Komma at the end because we have only one
    item in this list."""


"""Register our UserAdminClass to the User model"""
admin.site.register(models.User, UserAdmin)

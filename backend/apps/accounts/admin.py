from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EducatorProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Show our extra fields in the admin user form and list.
    fieldsets = UserAdmin.fieldsets + (
        ("Mentoria", {"fields": ("role", "preferred_language")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Mentoria", {"fields": ("email", "role")}),
    )
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = UserAdmin.list_filter + ("role",)


@admin.register(EducatorProfile)
class EducatorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "expertise")
    search_fields = ("user__username", "user__email", "expertise")

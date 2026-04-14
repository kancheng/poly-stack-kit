from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from hub.models import Execution, Rating, Task, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "name", "is_staff")
    search_fields = ("email", "name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profile", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "name")}),
    )


admin.site.register(Task)
admin.site.register(Execution)
admin.site.register(Rating)

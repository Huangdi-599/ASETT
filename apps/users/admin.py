from django.contrib import admin

from .models import PasswordResetToken


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "expires_at", "used_at", "created_at")
    search_fields = ("user__username", "user__email", "token")
    list_filter = ("used_at", "created_at")

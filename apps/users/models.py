from datetime import timedelta
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import TimestampedModel


def default_reset_expiry():
    return timezone.now() + timedelta(hours=1)


class PasswordResetToken(TimestampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField(default=default_reset_expiry)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    @property
    def is_expired(self) -> bool:
        return self.used_at is not None or timezone.now() >= self.expires_at

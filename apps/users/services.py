from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PasswordResetToken

User = get_user_model()


def register_user(*, username: str, email: str, password: str, first_name: str, last_name: str):
    validate_password(password)

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
    return user


def issue_token_pair(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": user,
    }


def create_password_reset_token(*, email: str):
    user = User.objects.filter(email__iexact=email, is_active=True).first()
    if user is None:
        return None

    token = PasswordResetToken.objects.create(user=user)
    return token


def confirm_password_reset(*, token: str, password: str, password_confirm: str):
    if password != password_confirm:
        raise ValidationError("Passwords do not match.")

    validate_password(password)
    reset_token = PasswordResetToken.objects.select_related("user").filter(token=token).first()

    if reset_token is None or reset_token.is_expired:
        raise ValidationError("Password reset token is invalid or expired.")

    user = reset_token.user
    user.set_password(password)
    user.save(update_fields=["password"])

    reset_token.used_at = timezone.now()
    reset_token.save(update_fields=["used_at", "updated_at"])
    return user


def build_password_reset_url(token: PasswordResetToken) -> str:
    return settings.PASSWORD_RESET_URL_TEMPLATE.format(token=token.token)

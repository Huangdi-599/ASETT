from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import PasswordResetToken
from .services import build_password_reset_url


@shared_task(name="apps.users.tasks.send_password_reset_email")
def send_password_reset_email(token_id: int) -> None:
    reset_token = PasswordResetToken.objects.select_related("user").get(id=token_id)
    reset_url = build_password_reset_url(reset_token)
    send_mail(
        subject="Reset your password",
        message=f"Use this link to reset your password: {reset_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reset_token.user.email],
    )

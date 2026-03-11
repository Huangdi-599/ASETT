from django.contrib.auth import get_user_model
from ninja.errors import HttpError
from ninja.security import HttpBearer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = AccessToken(token)
        except TokenError as exc:
            raise HttpError(401, "Invalid or expired access token.") from exc

        user = get_user_model().objects.filter(id=payload.get("user_id")).first()
        if user is None or not user.is_active:
            raise HttpError(401, "Authentication credentials were not provided.")

        request.user = user
        return user

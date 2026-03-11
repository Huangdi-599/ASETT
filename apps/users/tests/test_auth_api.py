import json

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import PasswordResetToken

pytestmark = pytest.mark.django_db

User = get_user_model()


def post_json(client: Client, path: str, payload: dict, **extra):
    return client.post(path, data=json.dumps(payload), content_type="application/json", **extra)


def get_auth_headers(user):
    access = str(RefreshToken.for_user(user).access_token)
    return {"HTTP_AUTHORIZATION": f"Bearer {access}"}


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="satoshi",
        email="satoshi@example.com",
        password="StrongPass123!",
        first_name="Satoshi",
        last_name="Nakamoto",
    )


def test_register_returns_token_pair_and_creates_user(client):
    response = post_json(
        client,
        "/api/v1/auth/register",
        {
            "username": "vitalik",
            "email": "vitalik@example.com",
            "password": "StrongPass123!",
            "first_name": "Vitalik",
            "last_name": "Buterin",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["access"]
    assert body["refresh"]
    assert body["user"]["username"] == "vitalik"
    assert User.objects.filter(username="vitalik", email="vitalik@example.com").exists()


def test_login_and_me_return_authenticated_user(client, user):
    login_response = post_json(
        client,
        "/api/v1/auth/login",
        {"username": user.username, "password": "StrongPass123!"},
    )

    assert login_response.status_code == 200
    access = login_response.json()["access"]

    me_response = client.get("/api/v1/auth/me", HTTP_AUTHORIZATION=f"Bearer {access}")

    assert me_response.status_code == 200
    assert me_response.json()["email"] == user.email


def test_logout_blacklists_refresh_token(client, user):
    refresh = str(RefreshToken.for_user(user))

    logout_response = post_json(
        client,
        "/api/v1/auth/logout",
        {"refresh": refresh},
        **get_auth_headers(user),
    )

    assert logout_response.status_code == 200
    assert logout_response.json()["detail"] == "You have been logged out successfully."

    refresh_response = post_json(client, "/api/v1/auth/refresh", {"refresh": refresh})

    assert refresh_response.status_code == 401
    assert refresh_response.json()["detail"] == "Refresh token is invalid or expired."


def test_password_reset_request_creates_token_and_sends_email(client, user, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.CELERY_TASK_ALWAYS_EAGER = True

    response = post_json(
        client,
        "/api/v1/auth/password-reset/request",
        {"email": user.email},
    )

    assert response.status_code == 200
    assert PasswordResetToken.objects.filter(user=user).count() == 1
    assert len(mail.outbox) == 1
    assert str(PasswordResetToken.objects.get(user=user).token) in mail.outbox[0].body


def test_password_reset_confirm_updates_credentials(client, user):
    reset_token = PasswordResetToken.objects.create(user=user)

    confirm_response = post_json(
        client,
        "/api/v1/auth/password-reset/confirm",
        {
            "token": str(reset_token.token),
            "password": "NewStrongPass123!",
            "password_confirm": "NewStrongPass123!",
        },
    )

    assert confirm_response.status_code == 200

    login_response = post_json(
        client,
        "/api/v1/auth/login",
        {"username": user.username, "password": "NewStrongPass123!"},
    )

    assert login_response.status_code == 200
    reset_token.refresh_from_db()
    assert reset_token.used_at is not None

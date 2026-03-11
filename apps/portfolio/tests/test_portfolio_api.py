import json
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

from apps.market.models import Asset
from apps.portfolio.models import Portfolio

pytestmark = pytest.mark.django_db

User = get_user_model()


def post_json(client: Client, path: str, payload: dict, **extra):
    return client.post(path, data=json.dumps(payload), content_type="application/json", **extra)


def patch_json(client: Client, path: str, payload: dict, **extra):
    return client.patch(path, data=json.dumps(payload), content_type="application/json", **extra)


def delete_json(client: Client, path: str, payload: dict | None = None, **extra):
    data = json.dumps(payload or {})
    return client.delete(path, data=data, content_type="application/json", **extra)


def get_auth_headers(user):
    access = str(RefreshToken.for_user(user).access_token)
    return {"HTTP_AUTHORIZATION": f"Bearer {access}"}


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="holder",
        email="holder@example.com",
        password="StrongPass123!",
    )


@pytest.fixture
def asset():
    return Asset.objects.create(
        external_id="bitcoin",
        symbol="BTC",
        name="Bitcoin",
        current_price=Decimal("65000.00"),
        market_cap=1_000_000,
        price_change_percentage_24h=Decimal("5.2500"),
        market_rank=1,
    )


def test_create_and_list_portfolios_for_current_user(client, user):
    create_response = post_json(
        client,
        "/api/v1/portfolios",
        {"name": "Main Wallet", "description": "Long-term holdings"},
        **get_auth_headers(user),
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "Main Wallet"
    assert created["holdings"] == []
    assert created["total_value"] == "0.00000000"

    list_response = client.get("/api/v1/portfolios", **get_auth_headers(user))

    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert items[0]["id"] == created["id"]


def test_add_update_and_delete_holding(client, user, asset):
    portfolio = Portfolio.objects.create(user=user, name="Trading")

    add_response = post_json(
        client,
        f"/api/v1/portfolios/{portfolio.id}/holdings",
        {"asset_id": asset.id, "quantity": "2.5"},
        **get_auth_headers(user),
    )

    assert add_response.status_code == 201
    added = add_response.json()
    assert added["total_value"] == "162500.00000000"
    assert len(added["holdings"]) == 1

    holding_id = added["holdings"][0]["id"]
    update_response = patch_json(
        client,
        f"/api/v1/portfolios/{portfolio.id}/holdings/{holding_id}",
        {"quantity": "3.0"},
        **get_auth_headers(user),
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["holdings"][0]["quantity"] == "3.00000000"
    assert updated["total_value"] == "195000.00000000"

    delete_response = delete_json(
        client,
        f"/api/v1/portfolios/{portfolio.id}/holdings/{holding_id}",
        **get_auth_headers(user),
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Holding deleted successfully."


def test_portfolio_endpoints_are_scoped_to_owner(client, user):
    other_user = User.objects.create_user(
        username="other",
        email="other@example.com",
        password="StrongPass123!",
    )
    portfolio = Portfolio.objects.create(user=other_user, name="Private")

    response = client.get(f"/api/v1/portfolios/{portfolio.id}", **get_auth_headers(user))

    assert response.status_code == 404

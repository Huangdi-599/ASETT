from decimal import Decimal

import pytest
from django.test import Client

from apps.market.models import Asset

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def seeded_assets():
    return [
        Asset.objects.create(
            external_id="bitcoin",
            symbol="BTC",
            name="Bitcoin",
            current_price=Decimal("65000.00"),
            market_cap=1_000_000,
            price_change_percentage_24h=Decimal("3.5000"),
            market_rank=1,
        ),
        Asset.objects.create(
            external_id="ethereum",
            symbol="ETH",
            name="Ethereum",
            current_price=Decimal("3500.00"),
            market_cap=500_000,
            price_change_percentage_24h=Decimal("7.2500"),
            market_rank=2,
        ),
        Asset.objects.create(
            external_id="solana",
            symbol="SOL",
            name="Solana",
            current_price=Decimal("150.00"),
            market_cap=250_000,
            price_change_percentage_24h=Decimal("-1.0000"),
            market_rank=3,
        ),
    ]


def test_list_assets_supports_search_and_limit(client, seeded_assets):
    response = client.get("/api/v1/assets", {"search": "eth", "limit": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["external_id"] == "ethereum"


def test_get_asset_returns_requested_item(client, seeded_assets):
    asset = seeded_assets[0]

    response = client.get(f"/api/v1/assets/{asset.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == asset.id
    assert body["symbol"] == "BTC"


def test_top_movers_orders_assets_by_24h_change(client, seeded_assets):
    response = client.get("/api/v1/top-movers", {"limit": 2})

    assert response.status_code == 200
    items = response.json()
    assert [item["external_id"] for item in items] == ["ethereum", "bitcoin"]

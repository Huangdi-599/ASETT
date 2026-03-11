from decimal import Decimal

from celery import shared_task
from django.utils import timezone

from apps.market.models import Asset

from .clients.coingecko import CoinGeckoClient


def sync_market_assets_now(*, per_page: int = 100) -> int:
    client = CoinGeckoClient()
    payload = client.fetch_market_assets(per_page=per_page)
    synced_at = timezone.now()

    for item in payload:
        Asset.objects.update_or_create(
            external_id=item["id"],
            defaults={
                "symbol": item["symbol"].upper(),
                "name": item["name"],
                "image_url": item.get("image", ""),
                "current_price": Decimal(str(item.get("current_price") or 0)),
                "market_cap": item.get("market_cap") or 0,
                "price_change_percentage_24h": (
                    Decimal(str(item["price_change_percentage_24h"]))
                    if item.get("price_change_percentage_24h") is not None
                    else None
                ),
                "market_rank": item.get("market_cap_rank"),
                "last_synced_at": synced_at,
            },
        )

    return len(payload)


@shared_task(name="apps.integrations.tasks.sync_market_assets")
def sync_market_assets() -> int:
    return sync_market_assets_now()

from django.conf import settings
import httpx


class CoinGeckoClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.COINGECKO_BASE_URL

    def fetch_market_assets(self, *, per_page: int = 100, page: int = 1):
        response = httpx.get(
            f"{self.base_url}/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": per_page,
                "page": page,
                "sparkline": "false",
            },
            timeout=15.0,
        )
        response.raise_for_status()
        return response.json()

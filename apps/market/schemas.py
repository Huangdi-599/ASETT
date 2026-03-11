from datetime import datetime
from decimal import Decimal
from typing import Optional

from ninja import Schema


class AssetOut(Schema):
    id: int
    external_id: str
    symbol: str
    name: str
    image_url: str
    current_price: Decimal
    market_cap: int
    price_change_percentage_24h: Optional[Decimal] = None
    market_rank: Optional[int] = None
    last_synced_at: Optional[datetime] = None


class AssetListOut(Schema):
    total: int
    items: list[AssetOut]

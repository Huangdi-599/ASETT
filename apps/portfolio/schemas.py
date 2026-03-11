from datetime import datetime
from decimal import Decimal
from typing import Optional

from ninja import Field, Schema


class PortfolioCreateInput(Schema):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field("", max_length=255)


class PortfolioUpdateInput(Schema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class HoldingCreateInput(Schema):
    asset_id: int
    quantity: Decimal = Field(..., gt=0)


class HoldingUpdateInput(Schema):
    quantity: Decimal = Field(..., gt=0)


class HoldingAssetOut(Schema):
    id: int
    external_id: str
    symbol: str
    name: str
    current_price: Decimal
    price_change_percentage_24h: Optional[Decimal] = None


class HoldingOut(Schema):
    id: int
    quantity: str
    current_value: str
    created_at: datetime
    updated_at: datetime
    asset: HoldingAssetOut


class PortfolioOut(Schema):
    id: int
    name: str
    description: str
    total_value: str
    created_at: datetime
    updated_at: datetime
    holdings: list[HoldingOut]

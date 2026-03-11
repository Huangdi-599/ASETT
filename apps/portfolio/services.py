from decimal import Decimal

from django.shortcuts import get_object_or_404

from apps.market.models import Asset

from .models import Holding, Portfolio

EIGHT_DECIMAL_PLACES = Decimal("0.00000001")


def normalize_decimal(value: Decimal) -> Decimal:
    return Decimal(format(value, ".8f"))


def format_decimal(value: Decimal) -> str:
    return format(normalize_decimal(value), ".8f")


def get_user_portfolios(user):
    return Portfolio.objects.filter(user=user).prefetch_related("holdings__asset")


def get_user_portfolio(user, portfolio_id: int):
    return get_object_or_404(
        Portfolio.objects.filter(user=user).prefetch_related("holdings__asset"),
        id=portfolio_id,
    )


def build_holding_payload(holding: Holding):
    return {
        "id": holding.id,
        "quantity": format_decimal(holding.quantity.quantize(EIGHT_DECIMAL_PLACES)),
        "current_value": format_decimal(holding.current_value.quantize(EIGHT_DECIMAL_PLACES)),
        "created_at": holding.created_at,
        "updated_at": holding.updated_at,
        "asset": {
            "id": holding.asset.id,
            "external_id": holding.asset.external_id,
            "symbol": holding.asset.symbol,
            "name": holding.asset.name,
            "current_price": holding.asset.current_price,
            "price_change_percentage_24h": holding.asset.price_change_percentage_24h,
        },
    }


def build_portfolio_payload(portfolio: Portfolio):
    holdings = list(portfolio.holdings.all())
    total_value = format_decimal(
        sum((holding.current_value for holding in holdings), Decimal("0")).quantize(
            EIGHT_DECIMAL_PLACES
        )
    )
    return {
        "id": portfolio.id,
        "name": portfolio.name,
        "description": portfolio.description,
        "total_value": total_value,
        "created_at": portfolio.created_at,
        "updated_at": portfolio.updated_at,
        "holdings": [build_holding_payload(holding) for holding in holdings],
    }


def add_holding(*, portfolio: Portfolio, asset_id: int, quantity):
    asset = get_object_or_404(Asset, id=asset_id)
    holding, created = Holding.objects.get_or_create(
        portfolio=portfolio,
        asset=asset,
        defaults={"quantity": quantity},
    )
    if not created:
        holding.quantity += quantity
        holding.save(update_fields=["quantity", "updated_at"])
    return holding

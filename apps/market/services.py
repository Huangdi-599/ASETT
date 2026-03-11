from django.db.models import Q, QuerySet

from .models import Asset


def get_asset_queryset(search: str | None = None) -> QuerySet[Asset]:
    queryset = Asset.objects.all().order_by("market_rank", "name")
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(symbol__icontains=search) | Q(external_id__icontains=search)
        )
    return queryset


def get_top_movers(limit: int):
    return Asset.objects.exclude(price_change_percentage_24h__isnull=True).order_by(
        "-price_change_percentage_24h",
        "market_rank",
    )[:limit]

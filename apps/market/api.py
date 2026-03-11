from django.shortcuts import get_object_or_404
from ninja import Query, Router

from .models import Asset
from .schemas import AssetListOut, AssetOut
from .services import get_asset_queryset, get_top_movers

router = Router(tags=["market"])


@router.get(
    "assets",
    response=AssetListOut,
    summary="List market assets",
)
def list_assets(request, search: str | None = None, limit: int = Query(20, ge=1, le=100)):
    queryset = get_asset_queryset(search)
    assets = list(queryset[:limit])
    return {"total": queryset.count(), "items": assets}


@router.get(
    "assets/{asset_id}",
    response=AssetOut,
    summary="Return a single market asset",
)
def get_asset(request, asset_id: int):
    return get_object_or_404(Asset, id=asset_id)


@router.get(
    "top-movers",
    response=list[AssetOut],
    summary="List the best performing assets by 24h change",
)
def top_movers(request, limit: int = Query(10, ge=1, le=50)):
    return list(get_top_movers(limit))

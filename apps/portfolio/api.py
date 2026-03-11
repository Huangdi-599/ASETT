from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from apps.users.auth import JWTBearer
from apps.users.schemas import MessageOut

from .models import Holding, Portfolio
from .schemas import (
    HoldingCreateInput,
    HoldingUpdateInput,
    PortfolioCreateInput,
    PortfolioOut,
    PortfolioUpdateInput,
)
from .services import add_holding, build_portfolio_payload, get_user_portfolio, get_user_portfolios

router = Router(tags=["portfolio"])
auth = JWTBearer()


@router.get(
    "portfolios",
    auth=auth,
    response=list[PortfolioOut],
    summary="List the current user's portfolios",
)
def list_portfolios(request):
    return [build_portfolio_payload(portfolio) for portfolio in get_user_portfolios(request.auth)]


@router.post(
    "portfolios",
    auth=auth,
    response={201: PortfolioOut, 400: MessageOut},
    summary="Create a new portfolio",
)
def create_portfolio(request, payload: PortfolioCreateInput):
    try:
        portfolio = Portfolio.objects.create(user=request.auth, **payload.model_dump())
    except IntegrityError as exc:
        raise HttpError(400, "You already have a portfolio with that name.") from exc

    portfolio = get_user_portfolio(request.auth, portfolio.id)
    return 201, build_portfolio_payload(portfolio)


@router.get(
    "portfolios/{portfolio_id}",
    auth=auth,
    response=PortfolioOut,
    summary="Return a portfolio with its holdings",
)
def get_portfolio(request, portfolio_id: int):
    return build_portfolio_payload(get_user_portfolio(request.auth, portfolio_id))


@router.patch(
    "portfolios/{portfolio_id}",
    auth=auth,
    response={200: PortfolioOut, 400: MessageOut},
    summary="Update a portfolio",
)
def update_portfolio(request, portfolio_id: int, payload: PortfolioUpdateInput):
    portfolio = get_user_portfolio(request.auth, portfolio_id)
    updates = payload.model_dump(exclude_none=True)
    for field, value in updates.items():
        setattr(portfolio, field, value)

    try:
        portfolio.save()
    except IntegrityError as exc:
        raise HttpError(400, "You already have a portfolio with that name.") from exc

    return build_portfolio_payload(get_user_portfolio(request.auth, portfolio_id))


@router.delete(
    "portfolios/{portfolio_id}",
    auth=auth,
    response=MessageOut,
    summary="Delete a portfolio",
)
def delete_portfolio(request, portfolio_id: int):
    portfolio = get_user_portfolio(request.auth, portfolio_id)
    portfolio.delete()
    return {"detail": "Portfolio deleted successfully."}


@router.post(
    "portfolios/{portfolio_id}/holdings",
    auth=auth,
    response={201: PortfolioOut, 404: MessageOut},
    summary="Add an asset holding to a portfolio",
)
def create_holding(request, portfolio_id: int, payload: HoldingCreateInput):
    portfolio = get_user_portfolio(request.auth, portfolio_id)
    add_holding(portfolio=portfolio, **payload.model_dump())
    return 201, build_portfolio_payload(get_user_portfolio(request.auth, portfolio_id))


@router.patch(
    "portfolios/{portfolio_id}/holdings/{holding_id}",
    auth=auth,
    response=PortfolioOut,
    summary="Set the quantity for a holding",
)
def update_holding(request, portfolio_id: int, holding_id: int, payload: HoldingUpdateInput):
    portfolio = get_user_portfolio(request.auth, portfolio_id)
    holding = get_object_or_404(Holding, id=holding_id, portfolio=portfolio)
    holding.quantity = payload.quantity
    holding.save(update_fields=["quantity", "updated_at"])
    return build_portfolio_payload(get_user_portfolio(request.auth, portfolio_id))


@router.delete(
    "portfolios/{portfolio_id}/holdings/{holding_id}",
    auth=auth,
    response=MessageOut,
    summary="Delete a holding from a portfolio",
)
def delete_holding(request, portfolio_id: int, holding_id: int):
    portfolio = get_user_portfolio(request.auth, portfolio_id)
    holding = get_object_or_404(Holding, id=holding_id, portfolio=portfolio)
    holding.delete()
    return {"detail": "Holding deleted successfully."}

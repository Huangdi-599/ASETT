from ninja import NinjaAPI
from ninja.errors import HttpError

from apps.market.api import router as market_router
from apps.portfolio.api import router as portfolio_router
from apps.users.api import router as users_router

api = NinjaAPI(
    title="Crypto Portfolio API",
    version="1.0.0",
    description=(
        "A backend-only API for user authentication, portfolio management, "
        "market asset discovery, and scheduled market-data synchronization."
    ),
    docs_url="/docs",
    openapi_url="/openapi.json",
)


@api.exception_handler(HttpError)
def http_error_handler(request, exc: HttpError):
    return api.create_response(request, {"detail": exc.message}, status=exc.status_code)


api.add_router("v1/auth/", users_router)
api.add_router("v1/", market_router)
api.add_router("v1/", portfolio_router)

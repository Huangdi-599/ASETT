from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.common.models import TimestampedModel


class Portfolio(TimestampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolios",
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(fields=("user", "name"), name="unique_portfolio_name_per_user")
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.name}"


class Holding(TimestampedModel):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="holdings",
    )
    asset = models.ForeignKey(
        "market.Asset",
        on_delete=models.CASCADE,
        related_name="holdings",
    )
    quantity = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal("0"))

    class Meta:
        ordering = ("asset__market_rank", "asset__name")
        constraints = [
            models.UniqueConstraint(fields=("portfolio", "asset"), name="unique_asset_per_portfolio")
        ]

    @property
    def current_value(self):
        return self.quantity * self.asset.current_price

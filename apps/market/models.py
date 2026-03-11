from decimal import Decimal

from django.db import models

from apps.common.models import TimestampedModel


class Asset(TimestampedModel):
    external_id = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=100, unique=True)
    image_url = models.URLField(blank=True)
    current_price = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal("0"))
    market_cap = models.BigIntegerField(default=0)
    price_change_percentage_24h = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
    )
    market_rank = models.PositiveIntegerField(null=True, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("market_rank", "name")

    def __str__(self) -> str:
        return f"{self.name} ({self.symbol.upper()})"

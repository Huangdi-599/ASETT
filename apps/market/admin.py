from django.contrib import admin

from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "symbol",
        "current_price",
        "price_change_percentage_24h",
        "market_rank",
        "last_synced_at",
    )
    search_fields = ("name", "symbol", "external_id")
    list_filter = ("last_synced_at",)

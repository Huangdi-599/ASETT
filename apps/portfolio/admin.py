from django.contrib import admin

from .models import Holding, Portfolio


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", "updated_at")
    search_fields = ("name", "user__username", "user__email")


@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "asset", "quantity", "created_at", "updated_at")
    search_fields = ("portfolio__name", "asset__name", "asset__symbol")

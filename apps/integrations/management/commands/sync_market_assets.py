from django.core.management.base import BaseCommand

from apps.integrations.tasks import sync_market_assets_now


class Command(BaseCommand):
    help = "Fetch market assets from CoinGecko and update the local asset catalog."

    def handle(self, *args, **options):
        count = sync_market_assets_now()
        self.stdout.write(self.style.SUCCESS(f"Synced {count} assets."))

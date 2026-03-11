# Market Sync

## Overview

Market asset data is fetched from CoinGecko through `apps.integrations.clients.coingecko.CoinGeckoClient` and persisted into `apps.market.models.Asset`.

## Sync paths

- Celery task: `apps.integrations.tasks.sync_market_assets`
- Direct function: `apps.integrations.tasks.sync_market_assets_now`
- Management command: `python manage.py sync_market_assets`

## Stored fields

Each sync updates or creates assets keyed by CoinGecko `id` and stores:

- symbol
- name
- image URL
- current price
- market cap
- 24h price change percentage
- market rank
- last sync timestamp

## Scheduling

`config.settings.base` defines an hourly Celery beat entry named `sync-market-assets-hourly`.

In local development, `CELERY_TASK_ALWAYS_EAGER = True` means queued tasks run immediately in-process. In a deployed environment, run a worker and beat process if eager execution is disabled.

## Failure handling

The CoinGecko client uses `httpx` and raises for non-success responses. Any production deployment should monitor task failures and consider retry policies if intermittent API errors become common.

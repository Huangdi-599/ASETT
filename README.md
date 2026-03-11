# Backend

This directory contains the new Django backend for the crypto portfolio API. It is built with Django 5, Django Ninja, JWT authentication, and a modular app structure for users, market data, portfolios, and external integrations.

## Features

- JWT-based auth with register, login, refresh, logout, and profile endpoints
- Password reset flow backed by token records and async email tasks
- Portfolio and holding management for authenticated users
- Market asset catalogue and top-mover endpoints
- CoinGecko sync via management command and Celery task
- OpenAPI schema plus interactive API docs

## Apps

- `apps.users`: registration, JWT auth, profile, and password reset flows
- `apps.market`: read-only asset catalogue and top-mover endpoints
- `apps.portfolio`: authenticated portfolio and holding management
- `apps.integrations`: CoinGecko sync client, Celery task, and management command

## Installation

Use the full setup guide here:

- `docs/setup.md`

Quick start:

1. Copy `.env.example` to `.env`
2. Run `uv sync --dev`
3. Run `uv run python manage.py migrate`
4. Run `uv run python manage.py runserver`

## API Docs

After starting the server locally:

- Interactive docs: `http://127.0.0.1:8000/api/docs`
- OpenAPI schema: `http://127.0.0.1:8000/api/openapi.json`
- Health check: `http://127.0.0.1:8000/health/`

## Useful commands

- `uv run python manage.py runserver`
- `uv run python manage.py migrate`
- `uv run python manage.py makemigrations`
- `uv run python manage.py check`
- `uv run python manage.py sync_market_assets`
- `uv run pytest`

## Docs

- `docs/setup.md`
- `docs/auth-flow.md`
- `docs/market-sync.md`

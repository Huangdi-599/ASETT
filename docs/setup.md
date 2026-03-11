# Setup

## Requirements

- Python 3.12+
- `uv`
- SQLite for local development or a Postgres-compatible `DATABASE_URL`
- Optional Redis if you later disable eager Celery execution outside local/test environments

## Installation

1. Open the backend directory:

```bash
cd backend
```

2. Copy the example environment file:

```bash
cp .env.example .env
```

3. Install dependencies and create the local environment with `uv`:

```bash
uv sync --dev
```

4. Apply database migrations:

```bash
uv run python manage.py migrate
```

5. Optional: create an admin user:

```bash
uv run python manage.py createsuperuser
```

## Run

Start the development server:

```bash
uv run python manage.py runserver
```

The backend will be available at:

- API root: `http://127.0.0.1:8000/api/`
- OpenAPI docs: `http://127.0.0.1:8000/api/docs`
- OpenAPI schema: `http://127.0.0.1:8000/api/openapi.json`
- Admin: `http://127.0.0.1:8000/admin/`
- Health check: `http://127.0.0.1:8000/health/`

## Useful commands

- Run tests: `uv run pytest`
- Run Django checks: `uv run python manage.py check`
- Create migrations: `uv run python manage.py makemigrations`
- Apply migrations: `uv run python manage.py migrate`
- Sync market assets manually: `uv run python manage.py sync_market_assets`

## Local behavior

- `config.settings.local` enables Django debug mode.
- `CELERY_TASK_ALWAYS_EAGER = True` keeps Celery tasks synchronous for local development.
- Password reset emails use Django's console email backend by default.

## Environment notes

The default `.env.example` values are suitable for local development:

- `DATABASE_URL=sqlite:///db.sqlite3` uses SQLite locally
- `DJANGO_SETTINGS_MODULE=config.settings.local` uses the local settings module
- `CELERY_TASK_ALWAYS_EAGER=True` runs background tasks in-process
- `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` prints password reset emails to the console

For production, switch to `config.settings.production`, provide a PostgreSQL `DATABASE_URL`, and configure real Redis and email credentials.

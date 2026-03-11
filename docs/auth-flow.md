# Auth Flow

## Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/password-reset/request`
- `POST /api/v1/auth/password-reset/confirm`

## Registration and login

`register` creates a Django user after checking for duplicate username and email values, then returns a Simple JWT access/refresh token pair plus the serialized user.

`login` authenticates with username and password and returns the same token payload shape.

## Authenticated requests

Protected endpoints use the custom `JWTBearer` class in `apps.users.auth`. Clients should send:

`Authorization: Bearer <access-token>`

The bearer token is validated with Simple JWT, then the corresponding Django user is attached to the request.

## Refresh and logout

`refresh` exchanges a valid refresh token for a new access token.

`logout` blacklists the submitted refresh token through `rest_framework_simplejwt.token_blacklist`, preventing future reuse.

## Password reset

1. `password-reset/request` looks up the active user by email.
2. If the user exists, a `PasswordResetToken` row is created.
3. A Celery task sends the reset URL built from `PASSWORD_RESET_URL_TEMPLATE`.
4. `password-reset/confirm` validates the token, checks expiry/usage, updates the password, and marks the token as used.

The request endpoint always returns the same success message so unknown email addresses are not exposed.

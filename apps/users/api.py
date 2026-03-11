from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ninja import Router
from ninja.errors import HttpError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .auth import JWTBearer
from .schemas import (
    LoginInput,
    LogoutInput,
    MessageOut,
    PasswordResetConfirmInput,
    PasswordResetRequestInput,
    RefreshInput,
    RefreshOut,
    RegisterInput,
    TokenPairOut,
    UserOut,
)
from .services import confirm_password_reset, create_password_reset_token, issue_token_pair, register_user
from .tasks import send_password_reset_email

router = Router(tags=["auth"])
auth = JWTBearer()
User = get_user_model()


@router.post(
    "register",
    response={201: TokenPairOut, 400: MessageOut},
    summary="Register a new account",
)
def register(request, payload: RegisterInput):
    if User.objects.filter(username__iexact=payload.username).exists():
        raise HttpError(400, "Username is already in use.")
    if User.objects.filter(email__iexact=payload.email).exists():
        raise HttpError(400, "Email is already in use.")

    try:
        user = register_user(**payload.model_dump())
    except ValidationError as exc:
        raise HttpError(400, "; ".join(exc.messages)) from exc

    return 201, issue_token_pair(user)


@router.post(
    "login",
    response={200: TokenPairOut, 401: MessageOut},
    summary="Exchange credentials for JWT tokens",
)
def login(request, payload: LoginInput):
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is None:
        raise HttpError(401, "Invalid username or password.")

    return issue_token_pair(user)


@router.post(
    "refresh",
    response={200: RefreshOut, 401: MessageOut},
    summary="Refresh an access token",
)
def refresh_token(request, payload: RefreshInput):
    serializer = TokenRefreshSerializer(data=payload.model_dump())
    try:
        serializer.is_valid(raise_exception=True)
    except Exception as exc:
        raise HttpError(401, "Refresh token is invalid or expired.") from exc

    return serializer.validated_data


@router.post(
    "logout",
    auth=auth,
    response={200: MessageOut, 401: MessageOut},
    summary="Blacklist a refresh token",
)
def logout(request, payload: LogoutInput):
    try:
        token = RefreshToken(payload.refresh)
        token.blacklist()
    except TokenError as exc:
        raise HttpError(401, "Refresh token is invalid or expired.") from exc

    return {"detail": "You have been logged out successfully."}


@router.get(
    "me",
    auth=auth,
    response=UserOut,
    summary="Return the current user profile",
)
def me(request):
    return request.auth


@router.post(
    "password-reset/request",
    response=MessageOut,
    summary="Send a password reset email",
)
def request_password_reset(request, payload: PasswordResetRequestInput):
    reset_token = create_password_reset_token(email=payload.email)
    if reset_token is not None:
        send_password_reset_email.delay(reset_token.id)

    return {
        "detail": "If an account exists for that email, a password reset message has been queued."
    }


@router.post(
    "password-reset/confirm",
    response={200: MessageOut, 400: MessageOut},
    summary="Reset a password using a reset token",
)
def confirm_reset(request, payload: PasswordResetConfirmInput):
    try:
        confirm_password_reset(**payload.model_dump())
    except ValidationError as exc:
        raise HttpError(400, "; ".join(exc.messages)) from exc

    return {"detail": "Password reset successful."}

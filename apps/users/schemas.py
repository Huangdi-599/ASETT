from datetime import datetime
from typing import Optional

from ninja import Field, Schema


class UserOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str


class RegisterInput(Schema):
    username: str = Field(..., min_length=3, max_length=150)
    email: str
    password: str = Field(..., min_length=8)
    first_name: str = ""
    last_name: str = ""


class LoginInput(Schema):
    username: str
    password: str


class RefreshInput(Schema):
    refresh: str


class LogoutInput(Schema):
    refresh: str


class TokenPairOut(Schema):
    access: str
    refresh: str
    user: UserOut


class RefreshOut(Schema):
    access: str
    refresh: Optional[str] = None


class PasswordResetRequestInput(Schema):
    email: str


class PasswordResetConfirmInput(Schema):
    token: str
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)


class PasswordResetTokenOut(Schema):
    token: str
    expires_at: datetime


class MessageOut(Schema):
    detail: str

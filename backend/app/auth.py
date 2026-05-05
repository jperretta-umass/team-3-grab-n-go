import os
import time
from collections.abc import Callable
from typing import cast

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth_schemas import AuthResponse, LoginRequest, RegisterRequest, TokenResponse
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
TOKEN_TTL_SECONDS = 60 * 60 * 24
AUTH_SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY", "dev-auth-secret-change-me")
AUTH_ALGORITHM: str = "HS256"


JwtEncode = Callable[[dict[str, object], str, str], str]
JwtDecode = Callable[[str, str, list[str]], dict[str, object]]

jwt_encode: JwtEncode = cast(
    JwtEncode,
    jwt.encode,  # type: ignore[reportUnknownMemberType]
)
jwt_decode: JwtDecode = cast(
    JwtDecode,
    jwt.decode,  # type: ignore[reportUnknownMemberType]
)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }
    return jwt_encode(payload, AUTH_SECRET_KEY, AUTH_ALGORITHM)


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    try:
        payload = jwt_decode(
            token,
            AUTH_SECRET_KEY,
            [AUTH_ALGORITHM],
        )
        user_id = int(cast(str, payload["sub"]))
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def user_to_auth_response(user: User) -> AuthResponse:
    return AuthResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        phone_num=user.phone_num,
        is_deliverer=user.has_deliverer_profile,
    )


def user_to_token_response(user: User) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(user.id),
        user=user_to_auth_response(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    normalized_email = normalize_email(str(payload.email))
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user_to_token_response(user)


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    normalized_email = normalize_email(str(payload.email))
    user = db.query(User).filter(User.email == normalized_email).first()

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if len(payload.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 bytes)")

    if len(payload.password.encode("utf-8")) < 8:
        raise HTTPException(status_code=400, detail="Password too short (min 8 bytes)")

    user = User(
        username=payload.username,
        email=normalized_email,
        phone_num=payload.phone_num,
        has_deliverer_profile=payload.is_deliverer,
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user_to_token_response(user)


@router.get("/me", response_model=AuthResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return user_to_auth_response(current_user)

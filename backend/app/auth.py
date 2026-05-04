from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth_schemas import AuthResponse, LoginRequest, RegisterRequest
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return AuthResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        phone_num=user.phone_num,
        is_deliverer=user.has_deliverer_profile,
    )


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if len(payload.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 bytes)")

    if len(payload.password.encode("utf-8")) < 8:
        raise HTTPException(status_code=400, detail="Password too short (min 8 bytes)")

    user = User(
        username=payload.username,
        email=payload.email,
        phone_num=payload.phone_num,
        has_deliverer_profile=payload.is_deliverer,
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return AuthResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        phone_num=user.phone_num,
        is_deliverer=user.has_deliverer_profile,
    )

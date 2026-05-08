from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    password: str
    phone_num: str | None = None
    is_deliverer: bool = False

    @field_validator("password")
    @classmethod

    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError(
                "Password must be at least 6 characters long"
            )

        if len(value) > 72:
            raise ValueError(
                "Password must be less than 72 characters"
            )

        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6, max_length=72)


class AuthResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_num: str | None = None
    is_deliverer: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthResponse

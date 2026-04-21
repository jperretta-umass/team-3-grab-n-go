from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    phone_num: str | None = None
    is_deliverer: bool = False


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_deliverer: bool
    phone_num: str
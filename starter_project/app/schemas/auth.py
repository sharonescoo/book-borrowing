from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=80)
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=80)
    email: EmailStr | None = None
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

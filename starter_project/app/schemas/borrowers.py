from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BorrowerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)


class BorrowerRead(BorrowerCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

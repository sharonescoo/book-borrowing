from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    isbn: str | None = Field(default=None, max_length=32)
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    total_copies: int = Field(ge=1)


class BookRead(BookCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    available_copies: int
    created_at: datetime

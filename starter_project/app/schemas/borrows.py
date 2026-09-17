from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BorrowCreate(BaseModel):
    book_id: int = Field(gt=0)
    borrower_id: int = Field(gt=0)
    due_at: datetime


class BorrowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    borrower_id: int
    borrowed_at: datetime
    due_at: datetime
    returned_at: datetime | None

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class LogEvent(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    message: str
    level: str = "INFO"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

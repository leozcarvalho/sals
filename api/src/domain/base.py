from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Base(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = Field(default="system", nullable=True)
    updated_by: str = Field(default="system", nullable=True)

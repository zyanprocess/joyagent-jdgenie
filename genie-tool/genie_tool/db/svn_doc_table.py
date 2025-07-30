from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, text
from sqlmodel import SQLModel, Field


class SvnDocSummary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    path: str = Field(unique=True, index=True)
    revision: str = Field(index=True)
    summary: Optional[str]
    tags: Optional[str]
    create_time: Optional[datetime] = Field(
        sa_type=DateTime, default=None, nullable=False, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )

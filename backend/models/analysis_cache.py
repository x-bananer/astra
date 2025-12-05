from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class AnalysisCache(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: str
    group_id: str = Field(foreign_key="group.id")
    start_date: Optional[str] = Field(default=None, index=True)
    result_json: str
    config_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
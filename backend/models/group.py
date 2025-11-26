from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Group(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class GroupIntegrationToken(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    group_id: str = Field(foreign_key="group.id")
    provider: str
    access_token: str
    repo_full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
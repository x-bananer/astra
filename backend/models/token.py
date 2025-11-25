from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class IntegrationToken(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    team_id: str = Field(foreign_key="team.id")
    provider: str  # trello / github / gitlab / etc.
    access_token: str
    refresh_token: str | None = None
    expires_at: str | None = None
    created_at: datetime | None
    
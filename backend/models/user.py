from sqlmodel import SQLModel, Field
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str
    name: str | None = None
    avatar: str | None = None
    group_id: str | None = Field(default=None, foreign_key="group.id")
    provider: str = "google"  # TODO Questinable if we need it now.
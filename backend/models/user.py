from sqlmodel import SQLModel, Field
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str
    name: str | None = None
    provider: str = "google"  # TODO Questinable if we need it now.
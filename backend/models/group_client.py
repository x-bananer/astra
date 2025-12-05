from sqlmodel import SQLModel, Field, UniqueConstraint

class GroupClient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    group_id: str = Field(foreign_key="group.id")
    provider: str
    access_token: str
    resource_ref: str
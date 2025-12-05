from sqlmodel import SQLModel, Field, UniqueConstraint

class GroupClient(SQLModel, table=True):
    # ensures each group can have only one client per provider (prevents duplicates).
    __table_args__ = (
        UniqueConstraint("group_id", "provider"),
    )

    id: int | None = Field(default=None, primary_key=True)
    group_id: str = Field(foreign_key="group.id")
    provider: str
    access_token: str
    resource_ref: str
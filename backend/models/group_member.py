from sqlmodel import SQLModel, Field

class GroupMember(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    group_id: str = Field(foreign_key="group.id")
    user_id: str = Field(foreign_key="user.id")
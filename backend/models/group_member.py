from sqlmodel import SQLModel, Field
import uuid

class GroupMember(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    group_id: str = Field(foreign_key="group.id")
    user_id: str = Field(foreign_key="user.id")
    role: str = "member"  # member / admin
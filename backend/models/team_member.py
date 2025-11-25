from sqlmodel import SQLModel, Field
import uuid

class TeamMember(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    team_id: str = Field(foreign_key="team.id")
    role: str = "member"  # Possible roles: member, admin. TODO Questinable if we need it now.
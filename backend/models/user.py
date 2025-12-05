from sqlmodel import SQLModel, Field
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    name: str | None = None
    avatar: str | None = None
    group_id: int | None = Field(default=None, foreign_key="group.id")
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class UserGroup(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

    users: List["User"] = Relationship(back_populates="group")


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    password: str
    first_name: str
    last_name: str
    profile_pic: Optional[str]
    is_staff: bool = Field(default=False)

    group_id: Optional[int] = Field(foreign_key="usergroup.id")
    group: Optional[UserGroup] = Relationship(back_populates="users")
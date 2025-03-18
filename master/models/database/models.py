from datetime import datetime
from typing import List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint


class Cities(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    code: str = Field(max_length=10, nullable=False, index=True)
    name: str = Field(max_length=30, nullable=False, index=True)
    is_active: bool = Field(default=True, index=True)
    last_updated_by: str = Field(max_length=50, nullable=False)
    last_updated_date: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (UniqueConstraint("code", "name"),)


class Roles(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    role: str = Field(max_length=20, nullable=False, index=True)
    is_active: bool = Field(default=True, index=True)
    last_updated_by: str = Field(max_length=50, nullable=False)
    last_updated_date: datetime = Field(default_factory=datetime.utcnow)

    subroles: List["SubRoles"] = Relationship(back_populates="role")

    __table_args__ = (UniqueConstraint("role"),)


class SubRoles(SQLModel,table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    role_id: int = Field(default=None,foreign_key="roles.id",nullable=False,index=True)
    sub_role_name: str = Field(max_length=30,nullable=False,index=True)
    sub_role_description: str = Field(max_length=100)
    is_active: bool = Field(default=True,index=True)
    last_updated_by: str = Field(max_length=50, nullable=False)
    last_updated_date: datetime = Field(default_factory=datetime.utcnow)

    role: Roles = Relationship(back_populates="subroles")

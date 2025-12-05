from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Portfolio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    user_profession: str
    user_photo: str
    user_about: str

class Technology(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    icon_src: str
    
    relations: list["EntityTechnology"] = Relationship(
        back_populates="technology",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    small_about: str
    big_about: str
    user_comment: str
    cover_src: str

    p_relations: list["Feature"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    ti_relations: list["TechnicalInfo"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    img_relations: list["ProjectImage"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Feature(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_project: int = Field(foreign_key="project.id")
    feat: str

    project: Optional[Project] = Relationship(
        back_populates="p_relations"
    )

class TechnicalInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_project: int = Field(foreign_key="project.id")
    info: str

    project: Optional[Project] = Relationship(
        back_populates="ti_relations"
    )

class ProjectImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_project: int = Field(foreign_key="project.id")
    src: str

    project: Optional[Project] = Relationship(
        back_populates="img_relations"
    )

class EntityTechnology(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_entity: int
    id_tech: int = Field(foreign_key="technology.id")
    type_entity: str

    technology: Optional[Technology] = Relationship(
        back_populates="relations"
    )

#------ Auth ------

class Admin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    
class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="admin.id")
    token: str
    revoked: bool = False
    expires_at: datetime
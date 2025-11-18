from sqlmodel import SQLModel, Field
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

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    small_about: str
    big_about: str
    user_comment: str
    cover_src: str

class Feature(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_project: int
    feat: str

class TechnicalInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_project: int
    info: str

class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_entity: int
    type_entity: str
    src: str

class EntityTechnology(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_entity: int
    id_tech: int
    type_entity: str

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
from sqlmodel import SQLModel, Field
from typing import Optional

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

class EntityTechnologies(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_entity: int
    id_tech: int
    type_entity: str
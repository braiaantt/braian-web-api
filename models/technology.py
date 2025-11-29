from sqlmodel import SQLModel
from pydantic import BaseModel

class TechnologyUpdate(SQLModel):
    name: str
    icon_src: str

class TechnologyRead(BaseModel):
    id: int
    name: str
    icon_src: str
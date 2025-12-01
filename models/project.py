from typing import Optional
from pydantic import BaseModel

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    small_about: Optional[str] = None
    big_about: Optional[str] = None
    user_comment: Optional[str] = None
    cover_src: Optional[str] = None

class ProjectCreate(BaseModel):
    name: str
    small_about: str
    big_about: str
    user_comment: str

class ProjectRead(BaseModel):
    id: int
    name: str
    small_about: str
    big_about: str
    user_comment: str
    cover_src: str
from sqlmodel import SQLModel
from typing import Optional

class PortfolioProject(SQLModel):
    id: int
    name: str
    small_about: str
    cover_src: str

class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    small_about: Optional[str] = None
    big_about: Optional[str] = None
    user_comment: Optional[str] = None
    cover_src: Optional[str] = None

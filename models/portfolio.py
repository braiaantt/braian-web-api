from sqlmodel import SQLModel
from typing import Optional, List
from database.tables import Technology
from models.project import PortfolioProject

class PortfolioUpdate(SQLModel):
    user_name: Optional[str] = None
    user_profession: Optional[str] = None
    user_photo: Optional[str] = None
    user_about: Optional[str] = None

class PortfolioRead(SQLModel):
    user_name: str
    user_profession: str
    user_photo: str
    user_about: str
    techs: List[Technology]
    projects: List[PortfolioProject]
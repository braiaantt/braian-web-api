from pydantic import BaseModel
from typing import Optional, List
from models.project import ProjectRead
from models.technology import TechnologyRead

class PortfolioUpdate(BaseModel):
    user_name: Optional[str] = None
    user_profession: Optional[str] = None
    user_photo: Optional[str] = None
    user_about: Optional[str] = None

class PortfolioRead(BaseModel):
    user_name: str
    user_profession: str
    user_photo: str
    user_about: str
    techs: List[TechnologyRead]
    projects: List[ProjectRead]
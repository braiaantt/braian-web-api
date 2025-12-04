from typing import Optional
from pydantic import BaseModel
from models.technology import TechnologyRead
from models.feature import FeatureRead
from models.technical_info import TechnicalInfoRead

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
    techs: list[TechnologyRead]
    feats: list[FeatureRead]
    technical_info: list[TechnicalInfoRead]

class PortfolioProjectRead(BaseModel):
    id: int
    name: str
    small_about: str
    big_about: str
    user_comment: str
    cover_src: str
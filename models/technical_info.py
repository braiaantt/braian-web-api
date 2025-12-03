from pydantic import BaseModel

class TechnicalInfoRead(BaseModel):
    id: int
    id_project: int
    info: str

class TechnicalInfoCreate(BaseModel):
    id_project: int
    info: str
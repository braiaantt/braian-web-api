from pydantic import BaseModel

class FeatureRead(BaseModel):
    id: int
    id_project: int
    feat: str

class FeatureCreate(BaseModel):
    id_project: int
    feat: str
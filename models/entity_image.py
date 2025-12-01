from pydantic import BaseModel
from models.entity_type import EntityType

class ImageRelation(BaseModel):
    entity_id: int
    entity_type: EntityType

class ImageRead(BaseModel):
    entity_id: int
    entity_type: EntityType
    img_path: str
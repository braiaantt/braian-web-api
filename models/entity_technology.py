from pydantic import BaseModel
from .entity_type import EntityType

class EntityTechnologyData(BaseModel):
    id_entity: int
    type_entity: EntityType
    id_tech: int

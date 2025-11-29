from sqlmodel import SQLModel
from .entity_type import EntityType

class EntityTechnologyData(SQLModel):
    id_entity: int
    type_entity: EntityType
    id_tech: int

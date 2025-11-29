from daos import EntityTechnologyDao
from sqlmodel import Session
from models import EntityTechnologyData
from database import EntityTechnology
from exceptions import EntityTechnologyCreationError, EntityTechnologyRelationNotExists
from services import TechnologyService

class EntityTechnologyService:
    def __init__(self, session: Session):
        self.session = session
        self.entity_technology_dao = EntityTechnologyDao(session)

    def get_relations(self, id_entity: int, type_entity: str):
        tech_ids = self.entity_technology_dao.get_tech_ids(id_entity, type_entity)
        technology_service = TechnologyService(self.session)

        technologies = [
            technology_service.get_technology_by_id(tech_id)
            for tech_id in tech_ids
        ]

        return technologies

    def relate_technology(self, data: EntityTechnologyData):
        relation = EntityTechnology(
            id_entity=data.id_entity,
            type_entity=data.type_entity,
            id_tech=data.id_tech
            )
        
        inserted = self.entity_technology_dao.insert_relation(relation)
        if not inserted:
            raise EntityTechnologyCreationError()
        
        return inserted
    
    def delete_relation(self, data: EntityTechnologyData):
        relation = self.entity_technology_dao.get_relation(data)
        if not relation:
            raise EntityTechnologyRelationNotExists()
        
        return self.entity_technology_dao.delete_entity_technology(relation)
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from database import EntityTechnology
from models.entity_technology import EntityTechnologyData

class EntityTechnologyDao:
    def __init__(self, session: Session):
        self.session = session

    def insert_relation(self, relation: EntityTechnology):
        try:
            self.session.add(relation)
            self.session.commit()
            self.session.refresh(relation)
            return relation
        
        except SQLAlchemyError as error:
            self.session.rollback()
            print("Error Insert EntityTechnology: ", error)
            return None
    
    def get_tech_ids(self, id_entity: int, type_entity: str):
        return self.session.exec(
            select(EntityTechnology.id_tech).where(
                EntityTechnology.id_entity == id_entity,
                EntityTechnology.type_entity == type_entity
            )
        )

    def get_relation(self, data: EntityTechnologyData):
        return self.session.exec(
            select(EntityTechnology).where(
                EntityTechnology.id_entity == data.id_entity,
                EntityTechnology.type_entity == data.type_entity,
                EntityTechnology.id_tech == data.id_tech
            )
        ).first()

        
    def delete_entity_technology(self, relation: EntityTechnology):
        try:
            self.session.delete(relation)
            self.session.commit()
            return True
        
        except SQLAlchemyError as error:
            self.session.rollback()
            print("Error Delete EntityTechnology", error)
            return False
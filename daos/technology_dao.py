from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from database.tables import Technology, EntityTechnology

class TechnologyDao:
    def __init__(self, session: Session):
        self.session = session

    def insert_technology(self, technology: Technology):
        try:
            self.session.add(technology)
            self.session.commit()
            self.session.refresh(technology)
            return technology

        except SQLAlchemyError as error:
            self.session.rollback()
            print("Error Insert Technology: ", error)
            return None
        
    def get_tech_ids(self, id_entity: int, type_entity: str):
        try:
            query = select(EntityTechnology.id_tech).where(
                (EntityTechnology.id_entity == id_entity) &
                (EntityTechnology.type_entity == type_entity)
            )
            results = self.session.exec(query).all()
            return results
        
        except SQLAlchemyError as error:
            print("Error Read EntityTechnology: ", error)
            return []

    def get_techs(self, tech_ids: list[int]):
        try:
            query = select(Technology).where(Technology.id.in_(tech_ids))
            results = self.session.exec(query).all()
            return results
        
        except SQLAlchemyError as error:
            print("Error Read Technology: ", error)
            return []
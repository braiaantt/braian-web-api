from sqlmodel import Session, select, delete
from sqlalchemy.exc import SQLAlchemyError
from database.tables import Technology

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
        
    def get_all_techs(self):
        return self.session.exec(select(Technology)).all()

    def get_entity_techs(self, tech_ids: list[int]):
        query = select(Technology).where(Technology.id.in_(tech_ids))
        return self.session.exec(query).all()
        
    def get_tech(self, tech_id: int):
        return self.session.get(Technology, tech_id)
        
    def delete_tech(self, tech_id):
        try:
            statement = delete(Technology).where(Technology.id == tech_id)
            result = self.session.exec(statement)
            self.session.commit()
            return result.rowcount > 0
        
        except SQLAlchemyError as error:
            self.session.rollback()
            print("Error Delete Technology: ", error)
            return False

    def update_tech(self, technology: Technology):
        try:
            #'technology' is already attached to the session from TechnologyService
            self.session.commit()
            self.session.refresh(technology)
            return technology
        
        except SQLAlchemyError as error:
            print("Error Update Technology: ", error)
            self.session.rollback()
            return None
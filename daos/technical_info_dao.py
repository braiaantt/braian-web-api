from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from database.tables import TechnicalInfo

class TechnicalInfoDao:
    def __init__(self, session: Session):
        self.session = session

    def add_technical_info(self, tech_info: TechnicalInfo):
        try:
            self.session.add(tech_info)
            self.session.commit()
            self.session.refresh(tech_info)
            return tech_info
        except SQLAlchemyError as error:
            print("Error Creating TechnicalInfo: ", error)


    def get_technical_info(self, info_id: int):
        return self.session.exec(
            select(TechnicalInfo)
            .where(TechnicalInfo.id == info_id)
            ).first()
    
    def delete_technical_info(self, tech_info: TechnicalInfo):
        try:
            self.session.delete(tech_info)
            self.session.commit()
            return True
        
        except SQLAlchemyError as error:
            print("Error Deleting TechnicalInfo: ", error)
            return False
    
    def get_all(self, project_id: int):
        return self.session.exec(
            select(TechnicalInfo)
            .where(TechnicalInfo.id_project == project_id)
            .order_by(TechnicalInfo.id)
        ).all()
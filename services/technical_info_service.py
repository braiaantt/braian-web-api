from sqlmodel import Session
from database.tables import TechnicalInfo
from daos.technical_info_dao import TechnicalInfoDao
from models.technical_info import TechnicalInfoCreate
from exceptions.exceptions import TechnicalInfoCreationError, TechnicalInfoDeletingError, TechnicalInfoNotFound

class TechnicalInfoService:
    def __init__(self, session: Session):
        self.technical_info_dao = TechnicalInfoDao(session)

    def add_technical_info(self, data: TechnicalInfoCreate):
        technical_info = TechnicalInfo(
            id_project=data.id_project,
            info=data.info
        )
        created = self.technical_info_dao.add_technical_info(technical_info)
        if not created:
            raise TechnicalInfoCreationError()
        
        return created
    
    def delete_technical_info(self, info_id: int):
        info = self.technical_info_dao.get_technical_info(info_id)
        if not info:
            raise TechnicalInfoNotFound()
        
        result = self.technical_info_dao.delete_technical_info(info)
        if not result:
            raise TechnicalInfoDeletingError()
        
        return
    
    def get_technical_info(self, project_id: int):
        return self.technical_info_dao.get_all(project_id)
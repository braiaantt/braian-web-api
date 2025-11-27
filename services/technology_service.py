from sqlmodel import Session
from daos import TechnologyDao
from database import Technology
from models import TechnologyUpdate
from exceptions import TechnologyNotExists, TechnologyDeletingError, TechnologyCreationError, TechnologyUpdatingError, InvalidContentType
from fastapi import UploadFile
from utils import FileManager

class TechnologyService:
    def __init__(self, session: Session):
        self.technologyDao = TechnologyDao(session)

    def get_all_technologies(self):
        return self.technologyDao.get_all_techs()

    async def insert_technology(self, tech_name: str, file: UploadFile):
        icon_src = await FileManager.save_technology_image(file)

        technology = Technology(name=tech_name, icon_src=icon_src)
        technology_created = self.technologyDao.insert_technology(technology)

        if not technology_created:
            raise TechnologyCreationError()
        
        return technology_created

    def update_technology(self, tech_id: int, data: TechnologyUpdate):
        technology = self.technologyDao.get_tech(tech_id)

        if not technology:
            raise TechnologyNotExists()
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(technology, key, value)

        technology_updated = self.technologyDao.update_tech(technology)

        if not technology_updated:
            raise TechnologyUpdatingError()
        
        return technology_updated


    def delete_technology(self, tech_id):
        exists = self.technologyDao.get_tech(tech_id)

        if not exists:
            raise TechnologyNotExists()
        
        result = self.technologyDao.delete_tech(tech_id)

        if not result:
            raise TechnologyDeletingError()
        
        return True
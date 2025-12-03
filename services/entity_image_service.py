from sqlmodel import Session
from daos.entity_image_dao import ProjectImageDao
from models.entity_image import ImageDelete
from database.tables import ProjectImage
from utils.file_manager import FileManager
from exceptions.exceptions import EntityImageCreationError, EntityImageNotFound, EntityImageDeletingError
from fastapi import UploadFile
import os

class ProjectImageService:
    def __init__(self, session: Session):
        self.project_image_dao = ProjectImageDao(session)

    def get_image_paths(self, id_project: int):
        return self.project_image_dao.get_image_paths(id_project)

    async def add_image(self, id_project: int, file: UploadFile):
        src_path = await FileManager.save_image(file, FileManager.PROJECT_FOLDER)
        image = ProjectImage(id_project=id_project, src=src_path)
        image_created = self.project_image_dao.add_image_relation(image)

        if not image_created:
            raise EntityImageCreationError()
        
        return image_created.src
    
    def delete_image(self, data: ImageDelete):
        image = self.project_image_dao.get_image(data.id_project, data.src)
        if not image:
            raise EntityImageNotFound()
        
        src = image.src.lstrip("/") 
        os.remove(src)
        
        success = self.project_image_dao.remove_image(image)
        if not success:
            raise EntityImageDeletingError()
        
        return True
    
from sqlmodel import Session
from daos.entity_image_dao import EntityImageDao
from models.entity_image import ImageRelation, ImageRead
from database.tables import Image
from utils.file_manager import FileManager
from exceptions.exceptions import EntityImageCreationError, EntityImageNotFound, EntityImageDeletingError
from fastapi import UploadFile
import os, json

class EntityImageService:
    def __init__(self, session: Session):
        self.entity_image_dao = EntityImageDao(session)

    def get_image_paths(self, image_data: ImageRelation):
        return self.entity_image_dao.get_image_paths(image_data)

    async def add_image(self, image_json: str, file: UploadFile):
        data = json.loads(image_json)
        image_data = ImageRelation(**data)
        src_path = await FileManager.save_image(file, FileManager.PROJECT_FOLDER)
        
        image = Image(id_entity=image_data.entity_id, type_entity=image_data.entity_type, src=src_path)
        image_created = self.entity_image_dao.add_image_relation(image)

        if not image_created:
            raise EntityImageCreationError()
        
        return image_created.src
    
    def delete_image(self, image_data: ImageRead):
        image = self.entity_image_dao.get_image(image_data)
        if not image:
            raise EntityImageNotFound()
        
        src = image.src.lstrip("/") 
        os.remove(src)
        
        success = self.entity_image_dao.remove_image_relation(image)
        if not success:
            raise EntityImageDeletingError()
        
        return True
    
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from database.tables import Image
from models.entity_image import ImageRead, ImageRelation

class EntityImageDao:
    def __init__(self, session: Session):
        self.session = session

    def add_image_relation(self, image: Image):
        try:
            self.session.add(image)
            self.session.commit()
            self.session.refresh(image)
            return image
        
        except SQLAlchemyError as error:
            print("Image Create Error: ", error)
            self.session.rollback()
            return None
        
    def get_image(self, image_data: ImageRead):
        image = self.session.exec(select(Image).where(
                Image.id_entity == image_data.entity_id,
                Image.type_entity == image_data.entity_type,
                Image.src == image_data.img_path
                )
            ).first()
        
        return image

    def get_image_paths(self, image_data: ImageRelation):
        paths = self.session.exec(select(Image.src).where(
                Image.id_entity == image_data.entity_id,
                Image.type_entity == image_data.entity_type
                )
            ).all()
        return paths

    def remove_image_relation(self, image: Image):
        try:
            self.session.delete(image)
            self.session.commit()
            return True
        
        except SQLAlchemyError as error:
            print("Image Delete Error: ", error)
            self.session.rollback()
            return False
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from database.tables import ProjectImage

class ProjectImageDao:
    def __init__(self, session: Session):
        self.session = session

    def add_image_relation(self, image: ProjectImage):
        try:
            self.session.add(image)
            self.session.commit()
            self.session.refresh(image)
            return image
        
        except SQLAlchemyError as error:
            print("Image Create Error: ", error)
            self.session.rollback()
            return None
        
    def get_image(self, id_project: int, src: str):
        image = self.session.exec(select(ProjectImage).where(
                ProjectImage.id_project == id_project,
                ProjectImage.src == src
                )
            ).first()
        
        return image

    def get_image_paths(self, id_project: int):
        paths = self.session.exec(
            select(ProjectImage.src)
            .where(ProjectImage.id_project == id_project)
            .order_by(ProjectImage.id)
            ).all()
        return paths

    def remove_image(self, image: ProjectImage):
        try:
            self.session.delete(image)
            self.session.commit()
            return True
        
        except SQLAlchemyError as error:
            print("Image Delete Error: ", error)
            self.session.rollback()
            return False
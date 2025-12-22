from daos.project_dao import ProjectDao
from sqlmodel import Session
from services.entity_technology_service import EntityTechnologyService
from services.feature_service import FeatureService
from services.technical_info_service import TechnicalInfoService
from services.entity_image_service import ProjectImageService
from exceptions import ProjectNotExists, ProjectDeletingError, ProjectUpdatingError, ProjectCreationError
from models.project import ProjectUpdate, ProjectCreate, ProjectRead
from models.technology import TechnologyRead
from models.feature import FeatureRead
from models.technical_info import TechnicalInfoRead
from database.tables import Project
from fastapi import UploadFile
from utils.file_manager import FileManager
import json, os

class ProjectService:
    def __init__(self, session: Session):
        self.project_dao = ProjectDao(session)
        self.session = session

    async def insert_project(self, project_json: str, file: UploadFile):
        project = await self.create_project(project_json, file)
        project_inserted = self.project_dao.insert_project(project)
        if not project_inserted:
            raise ProjectCreationError()
        
        return project_inserted

    def get_project(self, project_id):
        exists = self.project_dao.get_project(project_id)
        if not exists:
            raise ProjectNotExists()
        
        project = ProjectRead(
            id=exists.id,
            name=exists.name,
            small_about=exists.small_about,
            big_about=exists.big_about,
            user_comment=exists.user_comment,
            cover_src=exists.cover_src,
            techs=[],
            feats=[],
            technical_info=[],
            img_paths=[]
        )

        #get technologies
        entity_technology_service = EntityTechnologyService(self.session)
        techs = entity_technology_service.get_relations(project.id, "project")
        project.techs = [TechnologyRead.model_validate(t.model_dump()) for t in techs]
        

        #get feats
        feature_service = FeatureService(self.session)
        feats = feature_service.get_features(project.id)
        project.feats = [FeatureRead.model_validate(f.model_dump()) for f in feats]

        #get technical info
        technical_info_service = TechnicalInfoService(self.session)
        info = technical_info_service.get_technical_info(project.id)
        project.technical_info = [TechnicalInfoRead.model_validate(i.model_dump()) for i in info]

        #get img paths
        project_image_service = ProjectImageService(self.session)
        paths = project_image_service.get_image_paths(project.id)
        project.img_paths = list(paths)

        return project
    
    def update_project(self, project_id: int, data: ProjectUpdate):
        project = self.project_dao.get_project(project_id)
        if not project:
            raise ProjectNotExists()
            
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(project, key, value)

        project_updated = self.project_dao.update_project(project)
            
        if not project_updated:
            raise ProjectUpdatingError()
        
        return project_updated
        
    def delete_project(self, project_id):
        exists = self.project_dao.get_project(project_id)
        if not exists:
            raise ProjectNotExists()
        
        src = exists.cover_src.lstrip("/")
        os.remove(src)

        result = self.project_dao.delete_project(exists)

        if not result:
            raise ProjectDeletingError()
        
        return True
    
    #------ Helpers ------

    async def create_project(self, project_json: str, file: UploadFile):
        data = json.loads(project_json)
        project_data = ProjectCreate(**data)
        cover_src = await FileManager.save_image(file, FileManager.PROJECT_FOLDER)

        project = Project(
            name=project_data.name,
            small_about=project_data.small_about,
            big_about=project_data.big_about,
            user_comment=project_data.user_comment,
            cover_src=cover_src
        )
        return project
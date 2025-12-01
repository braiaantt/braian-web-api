from daos import ProjectDao
from sqlmodel import Session
from exceptions import ProjectNotExists, ProjectDeletingError, ProjectUpdatingError, ProjectCreationError
from models.project import ProjectUpdate, ProjectCreate
from database import Project
from fastapi import UploadFile
from utils import FileManager
import json

class ProjectService:
    def __init__(self, session: Session):
        self.project_dao = ProjectDao(session)

    async def insert_project(self, project_json: str, file: UploadFile):
        project = await self.create_project(project_json, file)
        project_inserted = self.project_dao.insert_project(project)
        if not project_inserted:
            raise ProjectCreationError()
        
        return project_inserted

    def get_project(self, project_id):
        project = self.project_dao.get_project(project_id)
        if not project:
            raise ProjectNotExists()
            
        return project
    
    def update_project(self, project_id: int, data: ProjectUpdate):
        project = self.project_dao.get_project(project_id)
        if not project:
            raise ProjectNotExists()
            
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items:
            setattr(project, key, value)

        project_updated = self.project_dao.update_project(project)
            
        if not project_updated:
            raise ProjectUpdatingError()
        
        return project_updated
        
    def delete_project(self, project_id):
        exists = self.project_dao.get_project(project_id)
        if not exists:
            raise ProjectNotExists()
        
        result = self.project_dao.delete_project(project_id)

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
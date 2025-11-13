from daos import ProjectDao
from sqlmodel import Session
from exceptions import ProjectNotExists, ProjectDeletingError, ProjectUpdatingError, ProjectCreationError
from models import ProjectUpdate
from database import Project

class ProjectService:
    def __init__(self, session: Session):
        self.project_dao = ProjectDao(session)

    def insert_project(self, project: Project):
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
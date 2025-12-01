from sqlmodel import Session, select, delete
from sqlalchemy.exc import SQLAlchemyError
from database.tables import Project

class ProjectDao:
    def __init__(self, session: Session):
        self.session = session

    def get_portfolio_projects(self):
        projects = self.session.exec(
                select(Project)
                ).all()

        return projects
        
    def get_project(self, project_id: int):
        try:
            project = self.session.exec(select(Project).where(Project.id == project_id))
            if not project:
                return None
            
            return project
        
        except SQLAlchemyError as error:
            print("Error Read Project: ", error)
            return None
    
    def insert_project(self, project: Project):
        try:
            self.session.add(project)
            self.session.commit()
            self.session.refresh(project)
            return project
        
        except SQLAlchemyError as error:
            print("Error Insert Porject: ", error)
            self.session.rollback()
            return None

    def delete_project(self, project_id):
        try:
            statement = delete(Project).where(Project.id == project_id)
            result = self.session.exec(statement)
            self.session.commit()
            return result > 0
        
        except SQLAlchemyError as error:
            print("Error Delete Project: ", error)
            self.session.rollback
            return False
        
    def update_project(self, project: Project):
        try:
            #'project' is already attached to the session from TechnologyService
            self.session.commit()
            self.session.refresh(project)
            return project
        
        except SQLAlchemyError as error:
            print("Error Update Project: ", error)
            self.session.rollback()
            return None
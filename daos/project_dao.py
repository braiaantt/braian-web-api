from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from database.tables import Project
from models.project import PortfolioProject

class ProjectDao:
    def __init__(self, session: Session):
        self.session = session

    def get_portfolio_projects(self):
        try:
            results = self.session.exec(
                select(Project.id, Project.name, Project.small_about, Project.cover_src)
                ).all()
            
            projects = [
                PortfolioProject(
                    id = project.id,
                    name = project.name,
                    small_about = project.small_about,
                    cover_src = project.cover_src
                ) for project in results
            ]

            return projects
        
        except SQLAlchemyError as error:
            print("Error Read Project: ", error)
            return []
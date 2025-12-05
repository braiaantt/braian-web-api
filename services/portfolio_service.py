from fastapi import UploadFile
from daos.portfolio_dao import PortfolioDao
from daos.project_dao import ProjectDao
from services.entity_technology_service import EntityTechnologyService
from models.portfolio import PortfolioRead
from models.technology import TechnologyRead
from models.project import PortfolioProjectRead
from database.tables import Portfolio
from exceptions import PortfolioUpdatingError, PortfolioCreationError, PortfolioAlreadyExistsError, PortfolioNotExists
from utils.file_manager import FileManager

class PortfolioService():
    def __init__(self, session):
        self.session = session
        self.portfolio_dao = PortfolioDao(session)
        self.project_dao = ProjectDao(session)


    def get_portfolio(self):

        base_portfolio = self.portfolio_dao.get_portfolio()

        if not base_portfolio:
            return None
        
        portfolio = PortfolioRead(
            user_name = base_portfolio.user_name,
            user_profession= base_portfolio.user_profession,
            user_about = base_portfolio.user_about,
            user_photo = base_portfolio.user_photo,
            techs = [],
            projects = []
        )

        #get technologies
        entity_tech_service = EntityTechnologyService(self.session)
        techs = entity_tech_service.get_relations(1, "portfolio")
        portfolio.techs = [
                TechnologyRead.model_validate(tech.model_dump())
                for tech in techs
            ]

        #get projects
        projects = self.project_dao.get_portfolio_projects()
        portfolio.projects = [
            PortfolioProjectRead.model_validate(project.model_dump())
            for project in projects
        ]

        return portfolio

    def insert_portfolio(self, new_portfolio: Portfolio):
        exists = self.portfolio_dao.get_portfolio()

        if exists:
            raise PortfolioAlreadyExistsError()

        created = self.portfolio_dao.insert_portfolio(new_portfolio)

        if not created:
            raise PortfolioCreationError()
        
        return created
        
    def update_portfolio(self, data: dict):
        exists = self.portfolio_dao.get_portfolio()

        if not exists:
            raise PortfolioNotExists()
        
        for key, value in data.items():
                setattr(exists, key, value)

        portfolio_updated = self.portfolio_dao.update_portfolio(exists)

        if not portfolio_updated:
            raise PortfolioUpdatingError()
            
        return portfolio_updated
    
    async def update_user_photo(self, _: int, file: UploadFile):
        exists = self.portfolio_dao.get_portfolio()
        if not exists:
            raise PortfolioNotExists()
        
        FileManager.remove_image(exists.user_photo)

        new_photo_path = await FileManager.save_image(file, FileManager.PORTFOLIO_FOLDER)
        exists.user_photo = new_photo_path

        updated = self.portfolio_dao.update_portfolio(exists)
        if not updated:
            raise PortfolioUpdatingError()
        
        return updated.user_photo

from daos import PortfolioDao, TechnologyDao, ProjectDao
from models.portfolio import PortfolioRead
from models.technology import TechnologyRead
from models.project import ProjectRead
from database import Portfolio
from exceptions import PortfolioUpdatingError, PortfolioCreationError, PortfolioAlreadyExistsError, PortfolioNotExists

class PortfolioService():
    def __init__(self, session):
        self.portfolio_dao = PortfolioDao(session)
        self.technology_dao = TechnologyDao(session)
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
        tech_ids = self.technology_dao.get_tech_ids(base_portfolio.id, "portfolio")
        techs = self.technology_dao.get_entity_techs(tech_ids)
        portfolio.techs = [
            TechnologyRead.model_validate(tech.model_dump())
            for tech in techs
        ]

        #get projects
        projects = self.project_dao.get_portfolio_projects()
        portfolio.projects = [
            ProjectRead.model_validate(project.model_dump())
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
        
        portfolio_updated = self.portfolio_dao.update_portfolio(data)

        if not portfolio_updated:
            raise PortfolioUpdatingError()
            
        return portfolio_updated
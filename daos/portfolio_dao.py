from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from database.tables import Portfolio

class PortfolioDao:
    def __init__(self, session: Session):
        self.session = session

    def insert_portfolio(self, portfolio: Portfolio):
        try:
            self.session.add(portfolio)
            self.session.commit()
            self.session.refresh(portfolio)
            return portfolio
        
        except SQLAlchemyError as error:
            self.session.rollback()
            print("Error Insert Portfolio: ", error)
            return None
        
    def update_portfolio(self, portfolio: Portfolio):
        try:
            self.session.commit()
            self.session.refresh(portfolio)
            return portfolio

        except SQLAlchemyError as error:
            self.session.rollback()
            print("Error Update Portfolio: ", error)
            return None            
    
    def get_portfolio(self):
        return self.session.exec(select(Portfolio)).first()

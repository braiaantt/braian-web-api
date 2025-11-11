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
        
    def update_portfolio(self, updates: dict):
        try:
            portfolio = self.session.exec(select(Portfolio)).first()

            if not portfolio:
                print("Error Update Portfolio: Not Exists")
                return None

            for key, value in updates.items():
                setattr(portfolio, key, value)

            self.session.add(portfolio)
            self.session.commit()
            self.session.refresh(portfolio)
            return portfolio

        except SQLAlchemyError as error:
            self.session.rollback()
            print("Error Update Portfolio: ", error)
            return None            
    
    def get_portfolio(self):
        try:
            portfolio = self.session.exec(select(Portfolio)).first()

            if  portfolio:
                return portfolio
            else:
                print("Error Update Portfolio: Not Exists")
                return None
            
        except SQLAlchemyError as error:
            print("Error Read Portfolio: ", error)
            return None
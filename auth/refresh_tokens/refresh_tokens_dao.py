from database import RefreshToken
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

class RefreshTokenDao:
    def __init__(self, session: Session):
        self.session = session

    def insert_refresh_token(self, token: RefreshToken):
        try:
            self.session.add(token)
            self.session.commit()
            self.session.refresh(token)
            return token
        
        except SQLAlchemyError as error:
            print("Error Insert RefreshToken: ", error)
            self.session.rollback()
            return None
        
    def get_refresh_token(self, admin_id: int, token: str):
        refresh_token = self.session.exec(select(RefreshToken).where(RefreshToken.admin_id == admin_id, RefreshToken.token == token)).first()
        if not refresh_token:
            return None
        
        return refresh_token
    
    def revoke_token(self, token: RefreshToken):
        try:
            token.revoked = True
            self.session.commit()
            self.session.refresh(token)
            return token
        
        except SQLAlchemyError as error:
            print("Error Revoke RefreshToken: ", error)
            self.session.rollback()
            return None        
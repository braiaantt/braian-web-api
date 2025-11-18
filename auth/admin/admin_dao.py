from sqlmodel import Session, select
from database import Admin

class AdminDao:
    def __init__(self, session: Session):
        self.session = session

    def get_admin(self, email: str):        
        admin = self.session.exec(
            select(Admin).where(Admin.email == email)
            ).first()
        return admin
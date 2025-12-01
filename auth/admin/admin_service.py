from .admin_dao import AdminDao
from sqlmodel import Session
from .admin_model import LoginData
from .admin_exceptions import AdminNotExists, InvalidCredentials
from utils.password_utils import verify_password

class AdminService:
    def __init__(self, session: Session):
        self.admin_dao = AdminDao(session)

    def get_admin(self, data: LoginData):
        admin = self.admin_dao.get_admin(data.email)
        if not admin:
            raise AdminNotExists()
        
        if not verify_password(data.password, admin.password):
            raise InvalidCredentials()

        return admin
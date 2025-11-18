from .refresh_tokens_dao import RefreshTokenDao
from sqlmodel import Session
from database import RefreshToken
from .refresh_token_exceptions import RefreshTokenCreationError, RefreshTokenRevokingError
from ..jwt_utils import extract_expire

class RefreshTokenService:
    def __init__(self, session: Session):
        self.refresh_token_dao = RefreshTokenDao(session)

    def insert_refresh_token(self, token: str, admin_id: int):
        expires_at = extract_expire(token)

        refresh_token = RefreshToken(
            admin_id=admin_id,
            token = token,
            expires_at=expires_at
            )
        
        token_inserted = self.refresh_token_dao.insert_refresh_token(refresh_token)
        if not token_inserted:
            raise RefreshTokenCreationError()
        
        return token_inserted

    def revoke_token(self, token: RefreshToken):
        revoked = self.refresh_token_dao.revoke_token(token)
        if not revoked:
            raise RefreshTokenRevokingError()

    def refresh_token_exists(self, admin_id: int, token: str):
        exists = self.refresh_token_dao.get_refresh_token(admin_id, token)

        if not exists:
            return None
        
        return exists
            
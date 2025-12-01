from fastapi import APIRouter, Depends, HTTPException
from database.db import get_session
from .admin.admin_service import AdminService
from .admin.admin_model import LoginData
from .admin.admin_exceptions import AdminNotExists, InvalidCredentials
from .refresh_tokens.refresh_token_exceptions import RefreshTokenCreationError,RefreshTokenRevoked, RefreshTokenRevokingError, RefreshTokenExpired
from .refresh_tokens.refresh_token_service import RefreshTokenService
from .exceptions import TokenInvalidType, TokenInvalidSignature
from .jwt_utils import create_access_token, create_refresh_token, validate_signature_and_type


router = APIRouter()

@router.post("/login", status_code=201)
def get_tokens(login_data: LoginData, session = Depends(get_session)):
    admin_service = AdminService(session)
    refresh_token_service = RefreshTokenService(session)

    try:
        admin = admin_service.get_admin(login_data)

        if admin:
            access_token = create_access_token(admin.id)
            refresh_token = create_refresh_token(admin.id)
            refresh_token_service.insert_refresh_token(refresh_token, admin.id)

            return{
                "access_token" : access_token,
                "refresh_token" : refresh_token,
                "token_type" : "bearer"
            }
            
    except AdminNotExists:
        raise HTTPException(status_code=404, detail="Admin Not Exists")
    
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    except TokenInvalidType:
        raise HTTPException(status_code=401, detail="Invalid Token Type")

    except RefreshTokenCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating Refresh Token")
    

@router.post("/refresh", status_code=201)
def refresh_token(client_token: str, session = Depends(get_session)):
    refresh_token_service = RefreshTokenService(session)
    try:
        validated_payload = validate_signature_and_type(client_token, "refresh")
        exists = refresh_token_service.refresh_token_exists(validated_payload["sub"], client_token)

        if not exists:
            raise HTTPException(status_code=404, detail="Refresh Token Not Exists")
        refresh_token_service.validate_exp_and_revoke(exists, validated_payload)
        refresh_token_service.revoke_token(exists)

        access_token = create_access_token(exists.admin_id)
        refresh_token = create_refresh_token(exists.admin_id)
        refresh_token_service.insert_refresh_token(refresh_token, exists.admin_id)

        return{
                "access_token" : access_token,
                "refresh_token" : refresh_token,
                "token_type" : "bearer"
            }

    except TokenInvalidSignature:
        raise HTTPException(status_code=401, detail="Invalid Token Singature")
    
    except TokenInvalidType:
        raise HTTPException(status_code=401, detail="Invalid Token Type")
    
    except RefreshTokenExpired:
        raise HTTPException(status_code=404, detail="Refresh Token Expired")
    
    except RefreshTokenRevoked:
        raise HTTPException(status_code=404, detail="Refresh Token Revoked")

    except RefreshTokenRevokingError:
        raise HTTPException(status_code=500, detail="Database Error Revoking Refresh Token")
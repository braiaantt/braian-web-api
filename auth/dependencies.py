from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from .jwt_utils import validate_access_token
from .exceptions import TokenExpired, TokenInvalidSignature, TokenInvalidType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def require_access_token(
        token: str = Depends(oauth2_scheme),
):
    try:
        payload = validate_access_token(token)
        return payload
    
    except TokenInvalidSignature:
        raise HTTPException(status_code=401, detail="Invalid Token Signature")
    
    except TokenInvalidType:
        raise HTTPException(status_code=401, detail="Invalid Token Type")
    
    except TokenExpired:
        raise HTTPException(status_code=401, detail="Access Token Expired")
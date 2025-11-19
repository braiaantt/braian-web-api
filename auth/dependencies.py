from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from .jwt_utils import validate_access_token
from .exceptions import TokenExpired, TokenInvalidSignature, TokenInvalidType

bearer_scheme = HTTPBearer()

async def require_access_token(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials
    
    try:
        payload = validate_access_token(token)
        return payload
    
    except TokenInvalidSignature:
        raise HTTPException(status_code=401, detail="Invalid Token Signature")
    
    except TokenInvalidType:
        raise HTTPException(status_code=401, detail="Invalid Token Type")
    
    except TokenExpired:
        raise HTTPException(status_code=401, detail="Access Token Expired")
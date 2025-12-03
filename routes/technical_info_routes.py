from fastapi import APIRouter, Depends, HTTPException
from models.technical_info import TechnicalInfoRead, TechnicalInfoCreate
from database.db import get_session
from auth.dependencies import require_access_token
from services.technical_info_service import TechnicalInfoService
from exceptions.exceptions import TechnicalInfoCreationError, TechnicalInfoDeletingError, TechnicalInfoNotFound

router = APIRouter()

@router.post("/technical-info", status_code=201, response_model=TechnicalInfoRead)
def add_technical_info(data: TechnicalInfoCreate, session = Depends(get_session), _ = Depends(require_access_token)):
    service = TechnicalInfoService(session)
    try:
        return service.add_technical_info(data)
    except TechnicalInfoCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating TechnicalInfo")
    
@router.delete("/technical-info/{info_id}")
def delete_technical_info(info_id: int, session = Depends(get_session), _ = Depends(require_access_token)):
    service = TechnicalInfoService(session)
    try:
        service.delete_technical_info(info_id)
        return
    except TechnicalInfoNotFound:
        raise HTTPException(status_code=404, detail="TechnicalInfo Not Found")
    except TechnicalInfoDeletingError:
        raise HTTPException(status_code=500, detail="Database Error Deleting Error")
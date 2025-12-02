from fastapi import APIRouter, Depends, HTTPException
from models.feature import FeatureCreate, FeatureRead
from database.db import get_session
from auth.dependencies import require_access_token
from services.feature_service import FeatureService
from exceptions.exceptions import FeatureCreationError, FeatureNotFound, FeatureDeletingError

router = APIRouter()

@router.post("/features", status_code=201, response_model=FeatureRead)
def add_feature(data: FeatureCreate, session = Depends(get_session), _ = Depends(require_access_token)):
    service = FeatureService(session)
    try:
        return service.add_feature(data)
    except FeatureCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating Feature")
    
@router.delete("/features/{feat_id}", status_code=204)
def delete_feature(feat_id: int, session = Depends(get_session), _ = Depends(require_access_token)):
    service = FeatureService(session)
    try:
        service.delete_feature(feat_id)
        return None
        
    except FeatureNotFound:
        raise HTTPException(status_code=404, detail="Feature To Delete Not Found")
    except FeatureDeletingError:
        raise HTTPException(status_code=500, detail="Database Error Deleting Feature")
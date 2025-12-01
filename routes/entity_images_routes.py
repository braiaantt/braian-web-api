from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from services.entity_image_service import EntityImageService
from models.entity_image import ImageRelation, ImageRead
from database.db import get_session
from auth.dependencies import require_access_token
from exceptions.exceptions import EntityImageCreationError, EntityImageNotFound, EntityImageDeletingError

router = APIRouter()

@router.get("/entity-image", status_code=200)
def get_entity_image_paths(
    data: ImageRelation = Depends(),
    session = Depends(get_session),
    _ = Depends(require_access_token)
    ):

    service = EntityImageService(session)
    return service.get_image_paths(data)

@router.post("/entity-image", status_code=201)
async def add_entity_image(
    json: str = Form(...),
    file: UploadFile = File(...),
    session = Depends(get_session),
    _ = Depends(require_access_token)
    ):

    service = EntityImageService(session)
    try:
        imgPath = await service.add_image(json, file)
        return imgPath

    except EntityImageCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating Entity Image")
    
@router.delete("/entity-image", status_code=204)
def delete_entity_image(
    data: ImageRead = Depends(),
    session = Depends(get_session),
    _ = Depends(require_access_token)
    ):

    service = EntityImageService(session)
    try:
        service.delete_image(data)
        return
    
    except EntityImageNotFound:
        raise HTTPException(status_code=404, detail="Image Requested To Delete Not Found")
    
    except EntityImageDeletingError:
        raise HTTPException(status_code=500, detail="Database Error Deleting Entity Image")
        
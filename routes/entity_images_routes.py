from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from services.entity_image_service import ProjectImageService
from models.entity_image import ImageRead, ImageDelete
from database.db import get_session
from auth.dependencies import require_access_token
from exceptions.exceptions import EntityImageCreationError, EntityImageNotFound, EntityImageDeletingError

router = APIRouter()

@router.post("/project-images", status_code=201)
async def add_entity_image(
    project_id: int = Form(...),
    file: UploadFile = File(...),
    session = Depends(get_session),
    _ = Depends(require_access_token)
    ):

    service = ProjectImageService(session)
    try:
        imgPath = await service.add_image(project_id, file)
        return imgPath

    except EntityImageCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating Entity Image")
    
@router.delete("/project-images", status_code=204)
def delete_entity_image(
    data: ImageDelete = Depends(),
    session = Depends(get_session),
    _ = Depends(require_access_token)
    ):

    service = ProjectImageService(session)
    try:
        service.delete_image(data)
        return
    
    except EntityImageNotFound:
        raise HTTPException(status_code=404, detail="Image Requested To Delete Not Found")
    
    except EntityImageDeletingError:
        raise HTTPException(status_code=500, detail="Database Error Deleting Entity Image")
        
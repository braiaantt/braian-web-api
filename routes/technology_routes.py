from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from database import get_session, Technology
from models import TechnologyUpdate
from services import TechnologyService
from exceptions import TechnologyNotExists, TechnologyCreationError, TechnologyUpdatingError, TechnologyDeletingError, InvalidContentType
from auth import require_access_token

router = APIRouter()

@router.get("/technology", status_code=200)
def get_technologies(session = Depends(get_session), _ = Depends(require_access_token)):
    service = TechnologyService(session)
    technologies = service.get_all_technologies()
    return {"data" : technologies}

@router.post("/technology", status_code=201)
async def insert_technology(
    name: str = Form(...),
    file: UploadFile = File(...), 
    session = Depends(get_session), 
    _ = Depends(require_access_token)
    ):

    service = TechnologyService(session)
    try:
        new_technology = await service.insert_technology(name, file)

        if new_technology:
            return {"data" : new_technology}
    
    except TechnologyCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating Technology")
    except InvalidContentType:
        raise HTTPException(status_code=400, detail="Invalid Content Type")


@router.put("/technology/{tech_id}", status_code=200)
def update_technology(tech_id: int, data: TechnologyUpdate, session = Depends(get_session), _ = Depends(require_access_token)):
    service = TechnologyService(session)
    try:
        updated_technology = service.update_technology(tech_id, data)
        
        if updated_technology:
            return {"data" : updated_technology}

    except TechnologyNotExists:
        raise HTTPException(status_code=404, detail="Technology Not Exists")
    
    except TechnologyUpdatingError:
        raise HTTPException(status_code=500, detail="Database Error Updating Technology")

@router.delete("/technology/{tech_id}", status_code=204)
def delete_technology(tech_id: int, session = Depends(get_session), _ = Depends(require_access_token)):
    service = TechnologyService(session)
    try:
        result = service.delete_technology(tech_id)
        
        if result:
            return
    
    except TechnologyNotExists:
        raise HTTPException(status_code=404, detail="Technology Not Exists")
    
    except TechnologyDeletingError:
        raise HTTPException(status_code=500, detail="Database Error Deleting Technology")
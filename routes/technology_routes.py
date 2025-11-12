from fastapi import APIRouter, Depends, HTTPException
from database import get_session, Technology
from models import TechnologyUpdate
from services import TechnologyService
from exceptions import TechnologyNotExists, TechnologyCreationError, TechnologyUpdatingError, TechnologyDeletingError

router = APIRouter()

@router.post("/technology", status_code=201)
def insert_technology(technology: Technology, session = Depends(get_session)):
    service = TechnologyService(session)
    try:
        new_technology = service.insert_technology(technology)

        if new_technology:
            return {"success" : True,
                    "data" : new_technology}
    
    except TechnologyCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating Technology")


@router.put("/technology/{tech_id}", status_code=200)
def update_technology(tech_id: int, data: TechnologyUpdate, session = Depends(get_session)):
    service = TechnologyService(session)
    try:
        updated_technology = service.update_technology(tech_id, data)
        
        if updated_technology:
            return {"success" : True,
                    "data" : updated_technology}

    except TechnologyNotExists:
        raise HTTPException(status_code=404, detail="Technology Not Exists")
    
    except TechnologyUpdatingError:
        raise HTTPException(status_code=500, detail="Database Error Updating Technology")

@router.delete("/technology/{tech_id}", status_code=20)
def delete_technology(tech_id: int, session = Depends(get_session)):
    service = TechnologyService(session)
    try:
        result = service.delete_technology(tech_id)
        
        if result:
            return {"success" : True}
    
    except TechnologyNotExists:
        raise HTTPException(status_code=404, detail="Technology Not Exists")
    
    except TechnologyDeletingError:
        raise HTTPException(status_code=500, detail="Database Error Deleting Technology")
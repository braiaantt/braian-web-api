from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
from services.project_service import ProjectService
from services.feature_service import FeatureService
from services.technical_info_service import TechnicalInfoService
from database.db import get_session
from exceptions import ProjectNotExists, ProjectCreationError, ProjectUpdatingError, ProjectDeletingError
from models.project import ProjectUpdate, ProjectRead
from models.feature import FeatureRead
from models.technical_info import TechnicalInfoRead
from auth.dependencies import require_access_token

router = APIRouter()

@router.get("/project/{project_id}", status_code=200)
def get_project(project_id: int, session = Depends(get_session)):
    service = ProjectService(session)
    try: 
        project = service.get_project(project_id)

        if project:
            return project
    
    except ProjectNotExists:
        raise HTTPException(status_code=404, detail="Project Not Exists")
    
@router.get("/project/{project_id}/features", status_code=200, response_model=list[FeatureRead])
def get_features(project_id, session = Depends(get_session), _ = Depends(require_access_token)):
    service = FeatureService(session)
    return service.get_features(project_id)

@router.get("/project/{project_id}/technical-info", status_code=200, response_model=list[TechnicalInfoRead])
def get_technical_info(project_id: int, session = Depends(get_session), _ = Depends(require_access_token)):
    service = TechnicalInfoService(session)    
    return service.get_technical_info(project_id)

@router.post("/project", status_code=201, response_model=ProjectRead)
async def insert_project(
    project: str = Form(...),
    file: UploadFile = File(...),
    session = Depends(get_session), 
    _ = Depends(require_access_token)
    ):

    service = ProjectService(session)
    try:
        new_project = await service.insert_project(project, file)
        if new_project:
            return new_project
        
    except ProjectCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating Project")
    
@router.put("/project/{project_id}", status_code=200)
def update_project(update_data: ProjectUpdate, session = Depends(get_session), _ = Depends(require_access_token)):
    service = ProjectService(session)
    try:
        project_updated = service.update_project(update_data)
        if project_updated:
            return project_updated
    
    except ProjectNotExists:
        raise HTTPException(status_code=404, detail="Project To Update Not Exists")
    
    except ProjectUpdatingError:
        raise HTTPException(status_code=500, detail="Database Error Updating Project")
    
@router.delete("project/{project_id}", status_code=204)
def delete_project(project_id: int, session = Depends(get_session), _ = Depends(require_access_token)):
    service = ProjectService(session)
    try: 
        result = service.delete_project(project_id)
        if result:
            return
    
    except ProjectNotExists:
        raise HTTPException(status_code=404, detail="Project To Delete Not Exists")

    except ProjectDeletingError:
        HTTPException(status_code=500, detail="Database Error Deleting Project")
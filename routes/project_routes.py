from fastapi import APIRouter, HTTPException, Depends
from services import ProjectService
from database import get_session, Project
from exceptions import ProjectNotExists, ProjectCreationError, ProjectUpdatingError, ProjectDeletingError
from models import ProjectUpdate
from auth import require_access_token

router = APIRouter()

@router.get("/project/{project_id}", status_code=200)
def get_project(project_id: int, session = Depends(get_session)):
    service = ProjectService(session)
    try: 
        project = service.get_project(project_id)

        if project:
            return {"success" : True,
                    "data" : project}
    
    except ProjectNotExists:
        raise HTTPException(status_code=404, detail="Project Not Exists")
    
@router.post("/project", status_code=201)
def insert_project(project: Project, session = Depends(get_session), _ = Depends(require_access_token)):
    service = ProjectService(session)
    try:
        new_project = service.insert_project(project)
        if new_project:
            return {"success" : True,
                    "data" : new_project}
        
    except ProjectCreationError:
        raise HTTPException(status_code=500, detail="Database Error Creating Project")
    
@router.put("/project/{project_id}", 200)
def update_project(update_data: ProjectUpdate, session = Depends(get_session), _ = Depends(require_access_token)):
    service = ProjectService(session)
    try:
        project_updated = service.update_project(update_data)
        if project_updated:
            return {"success" : True,
                    "data" : project_updated}
    
    except ProjectNotExists:
        raise HTTPException(status_code=404, detail="Project To Update Not Exists")
    
    except ProjectUpdatingError:
        raise HTTPException(status_code=500, detail="Database Error Updating Project")
    
@router.delete("project/{project_id}", status_code=200)
def delete_project(project_id: int, session = Depends(get_session), _ = Depends(require_access_token)):
    service = ProjectService(session)
    try: 
        result = service.delete_project(project_id)
        if result:
            return {"success" : True}
    
    except ProjectNotExists:
        raise HTTPException(status_code=404, detail="Project To Delete Not Exists")

    except ProjectDeletingError:
        HTTPException(status_code=500, detail="Database Error Deleting Project")
from fastapi import APIRouter, Depends, HTTPException
from models.entity_technology import EntityTechnologyData
from models.entity_type import EntityType
from models.technology import TechnologyRead
from database import get_session
from auth import require_access_token
from services import EntityTechnologyService
from exceptions import EntityTechnologyCreationError, EntityTechnologyRelationNotExists

router = APIRouter()

@router.get("/entity-technology", status_code=200, response_model=list[TechnologyRead])
def get_relations(id_entity: int, type_entity: EntityType, session = Depends(get_session), _ = Depends(require_access_token)):
    service = EntityTechnologyService(session)
    try:
        return service.get_relations(id_entity, type_entity)
    except Exception:
        raise HTTPException(status_code=404, detail="Entity Not Found")

@router.post("/entity-technology", status_code=201, response_model=EntityTechnologyData)
def relate_technology(data: EntityTechnologyData, session = Depends(get_session), _ = Depends(require_access_token)):
    service = EntityTechnologyService(session)
    try:
        return service.relate_technology(data)
    
    except EntityTechnologyCreationError:
        raise HTTPException(status_code=500, detail="Database Error Relating Entity With Technology")
    
@router.delete("/entity-technology", status_code=204)
def delete_relation(id_entity: int, type_entity: EntityType, id_tech: int,
                    session = Depends(get_session), _ = Depends(require_access_token)):
    service = EntityTechnologyService(session)
    try:
        data = EntityTechnologyData(
            id_entity=id_entity,
            type_entity=type_entity,
            id_tech=id_tech
        )
        result = service.delete_relation(data)

        if not result:
            raise HTTPException(status_code=500, detail="Database Error Deleting Relation")
        
        return

    except EntityTechnologyRelationNotExists:
        raise HTTPException(status_code=404, detail="Relation With Technology Not Exists")
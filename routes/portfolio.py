from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.db import get_session
from services.portfolio_service import PortfolioService

router = APIRouter()

@router.get("/portfolio", status_code=200)
def get_portfolio(session: Session = Depends(get_session)):
    service = PortfolioService(session)
    portfolio = service.get_portfolio()
    
    if portfolio:
        return {"success" : True,
                "data" : portfolio}
    
    raise HTTPException(status_code=404, detail="Portfolio Not Exists")
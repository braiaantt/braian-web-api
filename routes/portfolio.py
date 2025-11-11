from fastapi import APIRouter, HTTPException
from services.portfolio_service import PortfolioService
from database import db as db

router = APIRouter()

@router.get("/portfolio", status_code=200)
def get_portfolio():
    service = PortfolioService(db.get_session())
    portfolio = service.get_portfolio()
    
    if portfolio:
        return {"success" : True,
                "data" : portfolio}
    
    raise HTTPException(status_code=404, detail="Portfolio Not Exists")
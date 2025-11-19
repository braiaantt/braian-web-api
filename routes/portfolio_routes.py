from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session, Portfolio
from services import PortfolioService
from exceptions import PortfolioUpdatingError, PortfolioCreationError, PortfolioAlreadyExistsError, PortfolioNotExists
from auth import require_access_token

router = APIRouter()

@router.get("/portfolio", status_code=200)
def get_portfolio(session: Session = Depends(get_session)):
    service = PortfolioService(session)
    portfolio = service.get_portfolio()
    
    if portfolio:
        return {"data" : portfolio}
    
    raise HTTPException(status_code=404, detail="Portfolio Not Exists")

@router.post("/portfolio", status_code=201)
def add_portfolio(portfolio: Portfolio, session: Session = Depends(get_session), _ = Depends(require_access_token)):
    service = PortfolioService(session)
    try:
        portfolio = service.insert_portfolio(portfolio)
        if portfolio:
            return {"data" : portfolio}
    
    except PortfolioAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Portfolio Already Exists")
    except PortfolioCreationError:
        raise HTTPException(status_code=500, detail="Error Creating Portfolio")
        
@router.put("/portfolio", status_code=200)
def update_portfolio(data: dict, session: Session = Depends(get_session), _ = Depends(require_access_token)):
    service = PortfolioService(session)
    try:
        portfolio_updated = service.update_portfolio(data)
        if portfolio_updated:
            return {"data" : portfolio_updated}
        
    except PortfolioNotExists:
        raise HTTPException(status_code=404, detail="Inexistent Portfolio To Update")
    except PortfolioUpdatingError:
        raise HTTPException(status_code=409, detail="Internal Error Updating Portfolio")
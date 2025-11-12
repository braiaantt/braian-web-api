from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.db import get_session
from database.tables import Portfolio
from services.portfolio_service import PortfolioService
from exceptions.exceptions import (PortfolioCreationError, PortfolioAlreadyExistsError)

router = APIRouter()

@router.get("/portfolio", status_code=200)
def get_portfolio(session: Session = Depends(get_session)):
    service = PortfolioService(session)
    portfolio = service.get_portfolio()
    
    if portfolio:
        return {"success" : True,
                "data" : portfolio}
    
    raise HTTPException(status_code=404, detail="Portfolio Not Exists")

@router.post("/portfolio", status_code=201)
def add_portfolio(portfolio: Portfolio, session: Session = Depends(get_session)):
    service = PortfolioService(session)
    try:
        portfolio = service.add_portfolio(portfolio)
        if portfolio:
            return {"success" : True,
                    "data" : portfolio}
    
    except PortfolioAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Portfolio Already Exists")
    except PortfolioCreationError:
        raise HTTPException(status_code=500, detail="Error Creating Portfolio")
        
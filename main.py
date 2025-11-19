from fastapi import FastAPI
from routes import portfolio_router, technology_router
from auth import auth_router
from contextlib import asynccontextmanager
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(
    portfolio_router,
    tags=["Portfolio"]
)

app.include_router(
    technology_router,
    tags="Technology"
)

app.include_router(
    auth_router,
    tags=["Auth"]
)
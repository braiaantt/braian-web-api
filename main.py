from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import portfolio_router, technology_router, entity_technology_router
from auth import auth_router
from contextlib import asynccontextmanager
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    portfolio_router,
    tags=["Portfolio"]
)

app.include_router(
    technology_router,
    tags=["Technology"]
)

app.include_router(
    auth_router,
    tags=["Auth"]
)

app.include_router(
    entity_technology_router,
    tags=["EntityTechnology"]
)
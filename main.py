from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth.auth_routes import router as auth_router
from routes.entity_technologies_routes import router as entity_technology_router
from routes.portfolio_routes import router as portfolio_router
from routes.technology_routes import router as technology_router
from routes.project_routes import router as project_router
from routes.entity_images_routes import router as entity_image_router
from routes.feature_routes import router as features_router
from auth.auth_routes import router as auth_router
from contextlib import asynccontextmanager
from database.db import init_db

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

app.include_router(
    entity_image_router,
    tags=["EntityImage"]
)

app.include_router(
    project_router,
    tags=["Project"]
)

app.include_router(
    features_router,
    tags=["Features"]
)
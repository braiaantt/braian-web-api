from fastapi import FastAPI
from routes import portfolio_router
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
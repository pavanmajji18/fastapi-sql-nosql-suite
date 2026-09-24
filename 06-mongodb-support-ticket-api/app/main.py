from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import close_mongo_connection, connect_to_mongo
from app.routes import router as ticket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Open Mongo connection and build indexes
    await connect_to_mongo()
    yield
    # Shutdown: Close connection pool
    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Customer Support Ticket Management API with FastAPI and MongoDB.",
    lifespan=lifespan,
)

app.include_router(ticket_router)


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
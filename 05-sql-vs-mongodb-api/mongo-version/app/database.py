import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(
    settings.MONGODB_URL,
    tlsCAFile=certifi.where()
)
database = client[settings.DATABASE_NAME]

def get_db():
    return database
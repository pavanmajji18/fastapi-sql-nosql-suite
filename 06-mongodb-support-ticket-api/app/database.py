from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings


class DatabaseManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db_manager = DatabaseManager()


async def connect_to_mongo():
    db_manager.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_manager.db = db_manager.client[settings.DATABASE_NAME]

    # Create indexes for optimized search and filtering
    tickets = db_manager.db["tickets"]
    await tickets.create_index([("status", 1), ("priority", 1)])
    await tickets.create_index([("customer.email", 1)])
    # Text index for keyword search across title and description
    await tickets.create_index(
        [("title", "text"), ("description", "text"), ("tags", "text")],
        name="ticket_text_index",
    )


async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()


def get_database() -> AsyncIOMotorDatabase:
    return db_manager.db
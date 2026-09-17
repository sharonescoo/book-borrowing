from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db_name]


async def ping_mongo() -> None:
    await client.admin.command("ping")


async def get_logs_collection():
    return db[settings.mongo_logs_collection]

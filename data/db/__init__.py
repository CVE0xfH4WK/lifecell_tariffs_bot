from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from shared.config import config
from shared.logger import get_logger

logger = get_logger(__name__)


async def init_connection() -> None:
    logger.info(f'Creating a mongodb connection, {config.db.connection_string = }')

    client = AsyncIOMotorClient(config.db.connection_string)
    await init_beanie(
        database=client.db_name,
        document_models=[
            'data.db.models.Tariffs.Tariffs',
        ]
    )

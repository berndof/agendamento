import logging
from contextlib import asynccontextmanager

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from helpers.db import get_database_url

logger = logging.getLogger("app.db")

class Database:
    def __init__(self, db_url: str, engine_kwargs = {}):
        self.engine: AsyncEngine = create_async_engine(
            db_url,
            **engine_kwargs,
        )
        self.sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def close(self):
        await self.engine.dispose()


    @asynccontextmanager
    async def connect(self):
        async with self.engine.connect() as connection:
            try:
                yield connection
            except Exception as e:
                logger.error(f"Error in connection: {e}")
                await connection.rollback()
                raise 

    @asynccontextmanager
    async def session(self):
        async with self.sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                #logger.error(f"Error in session: {e}")
                await session.rollback()
                raise e

db = Database(get_database_url())

@asynccontextmanager
async def get_db_session_contextmanager():
    async with db.session() as session:
        yield session

async def get_db_session():
    async with db.session() as session:
        yield session
        
async def get_redis() -> Redis:
    #TODO
    redis_client: Redis = Redis(
        host="192.168.100.6",  # ou configuração da sua app
        port=6379,
        decode_responses=True  # importante se quiser strings em vez de bytes
    )
    
    return redis_client
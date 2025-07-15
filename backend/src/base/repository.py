import json
from typing import Any, TypeVar

from redis.asyncio import Redis
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable, text

from base.model import BaseModel
from base.schemas import BaseRedisSchema

T = TypeVar("T", bound=BaseModel)

class RedisRepository:
        
    @staticmethod
    async def redis_save_json(
        key: str, 
        value: Any,
        redis: Redis,
        expiration: int = 3600
    ) -> BaseRedisSchema:
        try:
            json_value = json.dumps(value)
            await redis.set(name=key, value=json_value, ex=expiration)
            result = BaseRedisSchema(key=key, value=json_value, expiration=expiration)
            return result
        except Exception as e:
            raise e

    @staticmethod
    async def redis_get_json_or_none(key: str, redis: Redis) -> str | None:
        try:
            result = await redis.get(key)
            if result is None:
                return None
            return str(result)
        except Exception as e:
            raise e

class BaseRepository(RedisRepository):

    @staticmethod
    async def save(
        obj: T,
        db_session: AsyncSession
    ) -> T:
        try:
            db_session.add(obj)
            await db_session.flush()
            await db_session.refresh(obj)
            return obj
        except Exception as e:
            raise e

    @staticmethod
    async def run_query(
        query: str | Executable,
        db_session: AsyncSession
    ) -> Result[tuple[T]]:
        if isinstance(query, str):
            query = text(query)

        result = await db_session.execute(query)
        return result

    @classmethod
    async def get_by(cls, model: type[T], db_session: AsyncSession, **kwargs:Any) -> Result[tuple[T]]:

        selection_query = select(model)
        
        #checar se os kwargs são atributos do modelo 
        for key, value in kwargs.items():
            if not hasattr(model, key):
                message = f"Model {model.__name__} has no attribute {key}"
                raise AttributeError(message)

            selection_query = selection_query.where(getattr(model, key) == value)

        result = await cls.run_query(selection_query, db_session)

        return result

    @classmethod
    async def get_all(cls, model: type[T], db_session: AsyncSession) -> Result[tuple[T]]:
        result = await cls.run_query(select(model), db_session)
        return result




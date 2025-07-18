import logging
import re
from typing import Any, Generic, TypeVar

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from base.model import BaseModel
from base.repository import BaseRepository
from base.schemas import BaseSchema

T = TypeVar("T", bound=BaseModel)

class BaseService:

    def __init__(
        self,
        _db_session: AsyncSession | None = None,
        _redis: Redis | None = None,
        _user_session: Any | None = None
    ) -> None:
        self._db_session = _db_session
        self._redis = _redis
        self._user_session = _user_session
        self.logger = logging.getLogger(f"app.service.{self.__class__.__name__}")

    @property
    def db_session(self) -> AsyncSession:
        if not self._db_session:
            self.logger.debug("No database session provided")
            raise RuntimeError("No database session provided")
        return self._db_session

    @property
    def redis(self) -> Redis:
        if not self._redis:
            self.logger.debug("No redis session provided")
            raise RuntimeError("No redis session provided")
        return self._redis

    @property
    def user_session(self) -> Any:
        if not self._user_session:
            self.logger.debug("No user session provided")
            raise RuntimeError("No user session provided")
        return self._user_session

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def _handle_integrity_error(self, ie:IntegrityError) -> HTTPException:
        detail = str(ie.orig)

        #captura os campos que causaram erro
        match = re.search(r'Key \((.*?)\)=', detail)
        if match:
            fields = [field.strip() for field in match.group(1).split(",")]
        else:
            fields = ["unknown"]
            self.logger.exception(detail)

        errors = {field: "already exists" for field in fields}
        return HTTPException(status_code=400, detail=errors)

    def _handle_exception(self, e: Exception) -> HTTPException:
        self.logger.exception(e)
        return HTTPException(status_code=500, detail=str(e))

class GenericService(BaseService ,Generic[T]):
    model: type[T] = None

    def __init__(self, db_session: AsyncSession | None = None, redis: Redis | None = None, *args, **kwargs):
        kwargs_super = {}
        if db_session is not None:
            kwargs_super["_db_session"] = db_session
        if redis is not None:
            kwargs_super["_redis"] = redis
        super().__init__(*args, **kwargs, **kwargs_super)

    async def create(self, new_data: BaseSchema) -> T:
        try:
            new_obj = self.model(**new_data.model_dump())
            new_obj = await BaseRepository.save(new_obj, db_session=self.db_session)

            #post create hook
            await self.post_create(new_obj)
            
            return new_obj
        except IntegrityError as ie:
            raise self._handle_integrity_error(ie)
        except Exception as e:
            raise self._handle_exception(e)

    async def post_create(self, obj: T):
        """Hook opcional chamado após criar um objeto. Deve ser sobrescrito nas subclasses."""
        pass

    async def get_or_create(self, new_data: Any, **kwargs:Any) -> tuple[T, bool]:
        try:
            return await self.get_one_by(**kwargs), False
        except NoResultFound:
            obj = await self.create(new_data)
            return obj, True

    async def get_one_by(self, **kwargs:Any) -> T:
        try:
            result = await BaseRepository.get_by(self.model, self.db_session, **kwargs)
            return result.scalars().one()
        except Exception as e:
            raise e

    async def get_all(self) -> list[T]:
        try:
            result = await BaseRepository.get_all(self.model, self.db_session)
            return result.scalars().all()
        except Exception as e:
            raise e
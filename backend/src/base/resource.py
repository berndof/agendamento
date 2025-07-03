import logging

from fastapi import APIRouter

from base.model import BaseModel


class BaseResource:
    model: type[BaseModel]
    router: APIRouter | None = None
    permissions: list[str] = ["read", "create", "update", "delete", "audit"]

    logger = logging.getLogger("app.resource")

    @classmethod
    def get_name(cls) -> str:
        return cls.model.__name__

    @classmethod
    def register(cls, router: APIRouter) -> None:
        if cls.router:
            router.include_router(cls.router)

    @classmethod
    def debug_(cls) -> None:
        cls.logger.debug(f"##### Resource: {cls.__name__} #####")
        cls.logger.debug(f"model: {cls.model.__name__}")
        if cls.router:
            cls.logger.debug(f"router: {cls.router.prefix}")
        cls.logger.debug(f"permissions: {cls.permissions}")
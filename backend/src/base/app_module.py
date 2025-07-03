import logging
from abc import ABCMeta, abstractmethod

from fastapi import APIRouter


class AppModule(metaclass=ABCMeta):
    router: APIRouter
    loader_priority: int = 0
    logger = logging.getLogger(f"app.mocule.{__name__}")
    module_path: str | None = None

    @classmethod
    def register(cls, root_router: APIRouter, module_path: str) -> None:
        if cls.router:
            root_router.include_router(cls.router)
        cls.module_path = module_path

    @classmethod
    @abstractmethod
    async def startup_hook(cls):
        pass

    @classmethod
    @abstractmethod
    async def seed_hook(cls):
        pass
    
    @classmethod
    def debug_(cls) -> None:
        cls.logger.debug(f"##### Module: {cls.__name__} #####")
        cls.logger.debug(f"router: {cls.router.prefix}")
        cls.logger.debug(f"priority: {cls.loader_priority}")
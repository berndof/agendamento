from app.core.access import routes
from base.app_module import AppModule


class AccessModule(AppModule):
    router = routes.router

    @classmethod
    async def startup_hook(cls):
        ...

    @classmethod
    async def seed_hook(cls):
        ...
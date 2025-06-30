import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI

from base.app_module import AppModule
from config import BASE_MODULE_PATHS
from helpers.modules import import_python_module

logger = logging.getLogger("app.factory.lifespan")

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    try:
        await ModuleRegistry.run_startup_hooks()
        logger.info("Server started - http://0.0.0.0:9090")
        yield
    finally:
        pass #perform shutdown tasks

class ModuleRegistry:
    _modules: list[type[AppModule]] = []

    @classmethod
    def register(cls, module: type[AppModule], api_router: APIRouter | None) -> None:
        """
        Registers a module with the module registry.

        If api_router is provided, the module's register method will be called with it.
        """
        cls._modules.append(module)
        if api_router:
            module.register(api_router)
            #logger.debug(f"Registered module {module.__name__}")

    @classmethod
    def get_modules(cls) -> list[type[AppModule]]:
        cls._modules.sort(key=lambda m: m.loader_priority)
        return cls._modules

    @classmethod
    def debug_modules_(cls) -> None:
        for module in cls.get_modules():
            module.debug_()

    @classmethod
    async def run_startup_hooks(cls) -> None:
        for module in cls.get_modules():
            if module.__dict__.get("startup_hook"):
                #logger.debug(f"Running startup hook for {module.__name__}")
                await module.startup_hook()

    @classmethod
    async def run_seed_hooks(cls) -> None:
        for module in cls.get_modules():
            hook = getattr(module, "seed_hook", None)
            if callable(hook):
                #logger.debug(f"Running seed hook for {module.__name__}")
                await module.seed_hook()


class App():
    def __init__(self,) -> None:
        ...

    def add_router(self):
        self.fastapi_app.include_router(self.router)
        return

    def init_fastapi(self) -> None:
        self.fastapi_app = FastAPI(lifespan=lifespan)
        self.router = APIRouter()
        return 

    def load_modules(self):
        for base_path in BASE_MODULE_PATHS:
            base_path = Path(base_path)

            for entry in base_path.iterdir():
                if not entry.is_dir():
                    continue

                if not (entry / "__init__.py").exists():
                    continue

                module_file = entry / "module.py"
                if not module_file.exists():
                    continue

                mod = import_python_module(module_file)
                if not mod:
                    continue

                for attr in dir(mod):
                    obj = getattr(mod, attr)
                    if isinstance(obj, type) and issubclass(obj, AppModule) and obj is not AppModule:
                        ModuleRegistry.register(obj, self.router)
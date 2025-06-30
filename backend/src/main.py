
import argparse
import asyncio
import logging

import uvicorn
import uvloop
from dotenv import load_dotenv
from fastapi import FastAPI

from app import App
from app.app import ModuleRegistry
from helpers.logs import setup_logs

load_dotenv()
setup_logs()

logger = logging.getLogger(__name__)

def set_parser():
    parser = argparse.ArgumentParser(description="Run fastapi server")

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Reload on file changes",
    )
    
    args = parser.parse_args()

    return args


def app_factory() -> FastAPI:

    app = App()
    app.init_fastapi()

    app.load_modules()
    ModuleRegistry.debug_modules_()
    app.add_router()


    return app.fastapi_app

def main() -> None:
 
    args = set_parser()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvicorn.run(
        app="main:app_factory",
        host="0.0.0.0",
        port=9090,
        reload=args.reload,
        factory=True,
        access_log=True, 
        log_level=logging.ERROR
    )

if __name__ == "__main__":
    main()
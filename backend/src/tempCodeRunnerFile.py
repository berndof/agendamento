
async def app_factory() -> FastAPI:

    app = App()
    await app.load_modules()
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
        factory=True
    )
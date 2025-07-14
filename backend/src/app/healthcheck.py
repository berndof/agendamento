from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])

@router.get("/")
async def healthcheck():
    return JSONResponse(status_code=200, content={"status": "ok"})


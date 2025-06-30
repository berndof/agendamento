from fastapi import APIRouter

router = APIRouter(prefix="/access", tags=["access"])


@router.get("/")
async def index():
    return {"message": "Hello from access"}
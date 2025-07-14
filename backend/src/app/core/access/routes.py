from fastapi import APIRouter

router = APIRouter(prefix="/access", tags=["access"])


@router.get("/")
async def index():
    return {"message": "Hello from access"}

@router.get("/foo")
async def foo():
    return {"message": "Hello from foo"}
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session, get_redis

router = APIRouter(prefix="/access", tags=["access"])


@router.get("/user/session/get-token")
async def user_session_get_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis),
):
    
    ...

@router.get("/")
async def index():
    return {"message": "Hello from access"}

@router.get("/foo")
async def foo():
    return {"message": "Hello from foo"}
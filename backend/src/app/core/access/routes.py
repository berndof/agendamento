from fastapi import APIRouter, BackgroundTasks, Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.access.resources.users.service import UserService
from app.core.access.schemas import (
    OauthPasswordSchema,
    UserRegisterResponse,
    UserRegisterSchema,
)
from app.core.access.service import AccessService
from app.db import get_db_session, get_redis

router = APIRouter(prefix="/access", tags=["access"])


@router.get("/user/session/get-token")
async def user_session_get_token(
    request: Request,
    form_data: OauthPasswordSchema = Depends(),
    db_session: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis),
):
    
    ...

@router.get("/")
async def index():
    return {"message": "Hello from access"}


@router.post("/register")
async def register(
    form_data: UserRegisterSchema,
    db_session: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):

    user_service = UserService(db_session=db_session)
    access_service = AccessService(_redis=redis)

    new_user = await user_service.create(form_data.user_data)
    await access_service.verify_new_user(new_user, background_tasks)
    return UserRegisterResponse(
        message=f"User create, a message will be sent to {new_user.email} to verify your account"
    )
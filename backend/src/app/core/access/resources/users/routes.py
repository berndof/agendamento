from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.access.resources.users.schemas import UserCreate, UserResponse
from app.core.access.resources.users.service import UserService
from app.db import get_db_session

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserResponse)
async def user_create(
    new_user_data: UserCreate,
    db_session: AsyncSession = Depends(get_db_session)
) -> UserResponse:
    
    user_service = UserService(db_session)

    new_user = await user_service.create(new_user_data)
    #add to default group
    return UserResponse(
        id=new_user.id.hex,
        status=new_user.status,
        created_at=new_user.created_at.isoformat(),
        username=new_user.username,
        email=new_user.email
    )

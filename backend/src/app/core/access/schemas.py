from __future__ import annotations

from fastapi.security import OAuth2PasswordBearer

from app.core.access.resources.users.schemas import UserCreate, UserSessionData
from base.schemas import BaseSchema

OauthPasswordSchema = OAuth2PasswordBearer(tokenUrl="/access/user/session/get-token")

class Token(BaseSchema):
    access_token: str
    token_type: str

class TokenPayload(BaseSchema):
    sub: str
    sid: str

class UsernameLogin(BaseSchema):
    username: str
    password: str

class UserSessionCache(BaseSchema):
    user_session_data: "UserSessionData"
    sid: str

class UserRegisterSchema(BaseSchema):
    user_data: "UserCreate"

class UserRegisterResponse(BaseSchema):
    message: str
    
    
UserRegisterSchema.model_rebuild()
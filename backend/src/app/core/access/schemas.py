from __future__ import annotations

from fastapi.security import OAuth2PasswordBearer

from app.core.access.resources.users.schemas import UserSessionData
from base.schemas import BaseSchema

OauthSchema = OAuth2PasswordBearer(tokenUrl="/access/user/session/get-token")

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


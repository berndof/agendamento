from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import EmailStr, Field, StringConstraints, field_validator

from base.schemas import BaseSchema
from helpers.password import get_password_hash

USERNAME_PATTERN = r"^[a-zA-Z0-9_]+$"

UsernameStr = Annotated[
    str,
    StringConstraints(min_length=3, max_length=30, pattern=USERNAME_PATTERN),
]

class UserStatusSchema(str, Enum):
    pending = "pending"
    active = "active"
    inactive = "inactive"
    blocked = "blocked"

class UserBase(BaseSchema):
    username: Annotated[
        UsernameStr,
        Field(..., example="myusername", description="Nome de usuário, entre 3 e 30 caracteres. Apenas letras, números e underscores."),
    ]

    email: Annotated[
        EmailStr,
        Field(..., example="example@example.com", description="Endereço de e-mail válido."),

    ]

class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(min_length=8, max_length=20)]

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        return get_password_hash(password)

    first_name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=50, pattern=r"^[A-Za-z]+$"),
        Field(..., example="John")
    ]  

    last_name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=50, pattern=r"^[A-Za-z]+$"),
        Field(..., example="Doe")
    ]

class UserResponse(UserBase):
    id: str
    status: UserStatusSchema
    created_at: str

class UserSessionData(UserBase):
    ...

UserSessionData.model_rebuild()
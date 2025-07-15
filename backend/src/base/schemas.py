from abc import ABC

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel, ABC):
    model_config = ConfigDict(from_attributes=True)

class BaseRedisSchema(BaseSchema):
    key: str = Field(..., description="Chave única no Redis.")
    value: str = Field(..., description="Valor associado à chave.")
    expiration: int | None = Field(
        None,
        description="Expiração em segundos (opcional). Se None, persiste indefinidamente.",
        ge=1
    )

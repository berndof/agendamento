import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import TIMESTAMP, UUID, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from base.model import BaseModel


class UserStatus(str, Enum):
    pending = "pending"
    active = "active"
    inactive = "inactive"
    blocked = "blocked"

class User(BaseModel):
    __tablename__ = "users"

    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc), server_default=func.now())
    status: Mapped[UserStatus] = mapped_column(SQLEnum(UserStatus), nullable=False, default=UserStatus.pending)


    #roles
    #groups
    #permissions
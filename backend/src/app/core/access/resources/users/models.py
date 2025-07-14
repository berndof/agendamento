from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from base.model import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
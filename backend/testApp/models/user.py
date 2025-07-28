from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Boolean


class User(Base):

    __table_args__ = {"extend_existing": True}
    username: Mapped[str] = mapped_column(String(30))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str]

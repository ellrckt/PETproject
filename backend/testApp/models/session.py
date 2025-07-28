from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import String, Integer
from models.base import Base


class UserSession(Base):

    __table_args__ = {"extend_existing": True}

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    exp: Mapped[int] = mapped_column(BigInteger, nullable=False)
    iat: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_blacklisted: Mapped[bool] = mapped_column(Boolean, default=False)

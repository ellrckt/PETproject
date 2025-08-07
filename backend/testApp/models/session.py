from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from geoalchemy2 import Geometry
from datetime import datetime
from sqlalchemy.types import Integer,String,DateTime,Boolean

class UserSession(Base):

    __table_args__ = {"extend_existing": True}

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    exp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    iat: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_blacklisted: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="sessions")
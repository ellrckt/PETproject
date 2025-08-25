from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy import String, Integer, LargeBinary, ForeignKey, Boolean, ARRAY
from typing import List

from models.base import Base


class UserPhoto(Base):
    __tablename__ = "user_photo"

    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profile.id"), nullable=False
    )
    profile: Mapped["Profile"] = relationship("Profile", back_populates="profile_photo")
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False, unique=True
    )
    s3_key: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

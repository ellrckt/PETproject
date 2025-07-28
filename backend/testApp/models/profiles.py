from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy import String, Integer, LargeBinary, ForeignKey
from models.base import Base


class Profile(Base):
    profile_img: Mapped[bytes] = mapped_column(LargeBinary)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="profile")

    def get_username(self):
        return self.user.username if self.user else None

    def get_email(self):
        return self.user.email if self.user else None
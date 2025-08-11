from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy import String, Integer, LargeBinary, ForeignKey,Boolean, ARRAY
from typing import List

from models.base import Base


class Profile(Base):
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[int] = mapped_column(Integer,nullable = True)
    city: Mapped[str] = mapped_column(String,nullable = True)
    country: Mapped[str] = mapped_column(String,nullable = True)
    about_user: Mapped[str] = mapped_column(String,nullable=True)
    user_habits: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="profile")
    # email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    
    # password: Mapped[str] = mapped_column(String(128), nullable=False)
    # email_is_confirmed: Mapped[bool] = mapped_column(Boolean,default = False)
    # profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False)
    #     return self.user.username if self.user else None

    # def get_email(self):
    #     return self.user.email if self.user else None 
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean

class User(Base):
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email_is_confirmed: Mapped[bool] = mapped_column(Boolean,default = False)
    # profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False)
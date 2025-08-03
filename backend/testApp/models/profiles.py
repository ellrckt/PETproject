from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy import String, Integer, LargeBinary, ForeignKey,Boolean

from models.base import Base


class Profile(Base):
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[str] = mapped_column(Integer,nullable = False)
    city: Mapped[str] = mapped_column(String,nullable = False)
    about_user: Mapped[str] = mapped_column(String,nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # password: Mapped[str] = mapped_column(String(128), nullable=False)
    # email_is_confirmed: Mapped[bool] = mapped_column(Boolean,default = False)
    # profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False)
    #     return self.user.username if self.user else None

    # def get_email(self):
    #     return self.user.email if self.user else None 
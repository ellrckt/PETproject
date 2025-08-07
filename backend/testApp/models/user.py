from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean
# from models.session import UserSession
# from models.location import UserLocation
class User(Base):

    __tablename__ = 'user'
    
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email_is_confirmed: Mapped[bool] = mapped_column(Boolean,default = False)
    sessions: Mapped[list["UserSession"]] = relationship("UserSession", back_populates="user")
    locations: Mapped["UserLocation"] = relationship(
        "UserLocation", 
        back_populates="user", 
        cascade="all, delete-orphan"  
    )
    # profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False)
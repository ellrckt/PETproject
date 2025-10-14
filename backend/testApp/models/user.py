from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Boolean, Integer
from models.session import UserSession
from models.location import UserLocation
from models.habits import Habits
from models.profiles import Profile
from models.subscription import Subscription

class User(Base):

    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(30), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email_is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    subscribers_count: Mapped[int] = mapped_column(Integer, default=0)
    subscriptions_count: Mapped[int] = mapped_column(Integer, default=0)


    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession", back_populates="user"
    )
    locations: Mapped["UserLocation"] = relationship(
        "UserLocation", back_populates="user", cascade="all, delete-orphan"
    )
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", cascade="all, delete-orphan"
    )
    subscriptions = relationship(
        "Subscription", 
        foreign_keys="Subscription.subscriber_id",
        back_populates="subscriber"
    )
    subscribers = relationship(
        "Subscription",
        foreign_keys="Subscription.target_id", 
        back_populates="target"
    )


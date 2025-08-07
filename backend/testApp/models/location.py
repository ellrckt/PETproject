from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.types import String, Boolean
from models.user import User
from typing import Optional

class UserLocation(Base):
    __tablename__ = "user_locations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    geom: Mapped[Optional[str]] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326),  
        nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="locations")
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
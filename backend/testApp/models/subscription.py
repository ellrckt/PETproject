# models/subscription.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
import enum

class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    PENDING = "pending" 
    BLOCKED = "blocked"

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    target_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    subscriber = relationship("User", foreign_keys=[subscriber_id], back_populates="subscriptions")
    target = relationship("User", foreign_keys=[target_id], back_populates="subscribers")
    
    __table_args__ = (
        UniqueConstraint('subscriber_id', 'target_id', name='unique_subscription'),
    )
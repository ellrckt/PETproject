# models/message.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, text
from pgvector.sqlalchemy import Vector
from datetime import datetime
from models.base import Base

class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, index=True)
    
    message: Mapped[str] = mapped_column(String(1000), nullable=False)
    room_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("NOW()"), nullable=False)
    is_viewed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    embedding: Mapped[list[float] | None] = mapped_column(Vector(384), nullable=True)
    
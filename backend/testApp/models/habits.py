from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from sqlalchemy import String, Integer, LargeBinary, ForeignKey,Boolean, ARRAY
from typing import List

from models.base import Base


class Habits(Base):

    name: Mapped[str] = mapped_column(String,nullable = False)

from abc import ABC, abstractmethod
from db.db import db_helper
from sqlalchemy import select, insert
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class AbstractProfileRepository(ABC):

    @abstractmethod
    async def add_one(data: dict):
        raise NotImplementedError


class ProfileRepository(AbstractProfileRepository):

    model = Profile

from utils.repository import SQLAlchemySessionRepository
from models.session import UserSession


class UserRepository(SQLAlchemySessionRepository):
    model = UserSession

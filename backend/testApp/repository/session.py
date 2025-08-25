from utils.repository import SQLAlchemySessionRepository
from models.session import UserSession


class SessionRepository(SQLAlchemySessionRepository):
    model = UserSession

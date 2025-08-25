from utils.auth_repository import SQLAlchemyAuthRepository 
from models.user import User


class AuthRepository(SQLAlchemyAuthRepository):
    model = User


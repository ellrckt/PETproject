from utils.user_repository import SQLAlchemyUserRepository,SQLAlchemyUserCRUDRepository
from models.user import User


class UserRepository(SQLAlchemyUserRepository):
    model = User

class UserCRUDRepository(SQLAlchemyUserCRUDRepository):
    model = User
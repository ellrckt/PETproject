from utils.profile_repository import SQLAlchemyProfileRepository
from models.profiles import Profile


class ProfileRepository(SQLAlchemyProfileRepository):
    model = Profile

from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path
from pydantic import PostgresDsn

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseSettings):

    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 4320
    google_client_id: str = "1078824262976-9g570h5ucqnrug3rfi9r98t7o6gqi4a4.apps.googleusercontent.com"
    google_client_secret: str = "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"

class Settings(BaseSettings):

    auth_jwt: AuthJWT = AuthJWT()


class DataBase(BaseSettings):
    url: str = "postgresql+asyncpg://admin:admin@localhost:5432/pet_db"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


settings = Settings()
db = DataBase()

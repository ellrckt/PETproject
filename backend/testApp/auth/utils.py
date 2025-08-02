import jwt
from config import settings
import bcrypt
from datetime import timedelta, datetime
from fastapi import HTTPException

ACCESS_TOKEN_TYPE = "access_token"
REFRESH_TOKEN_TYPE = "refresh_token"


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_days: int = settings.auth_jwt.refresh_token_expire_days,
    expire_timedelta: timedelta | None = None,
):
    if payload["token_type"] == REFRESH_TOKEN_TYPE:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(days=expire_days)
        to_encode.update(exp=expire, iat=now)
        encoded_jwt = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
    if payload["token_type"] == ACCESS_TOKEN_TYPE:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(exp=expire, iat=now)
        encoded_jwt = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
    return encoded_jwt


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    try:
        decoded_jwt = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has been expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def hash_password(password: str) -> str:

    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt).decode()


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password.encode()
    )

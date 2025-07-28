from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreation(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: EmailStr
    password: str


class UserResponse(UserCreation):
    model_config = ConfigDict(strict=True)
    id: int
    password: str


class UserRegistration(UserCreation):
    model_config = ConfigDict(strict=True)
    repit_password: str


class UserLogin(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: str


class UserUpdate(BaseModel):

    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreation(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: EmailStr
    password: str

class UserLocation(BaseModel):
    model_config = ConfigDict(strict=True)
    lat: float
    lng: float

class UserCityCountry(BaseModel):
    country: str
    city: str

class GetUser(BaseModel):
    pass



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


# class UserEmailConffirmation(BaseModel):
    
#     confirmation_code: str
#     typed_code: str

# class GCode(BaseModel):
#     code: str

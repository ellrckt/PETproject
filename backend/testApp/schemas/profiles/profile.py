from pydantic import BaseModel
from fastapi import UploadFile


class Profile(BaseModel):

    username: str
    age: int
    city: str
    country: str
    about_user: str
    user_habits: list
    user_id: int

class UpdateProfile(BaseModel):
    
    username: str | None
    age: int | None
    city: str | None
    country: str | None
    about_user: str | None
    user_habits: list | None

class EditProfile(BaseModel):
    profile_img: UploadFile | None = None
    username: str | None = None
    email: str | None = None
    # password: str | None = None

class Hobbies(BaseModel):
    name: str
from pydantic import BaseModel,  Field
from fastapi import UploadFile
from typing import Optional, List

class Profile(BaseModel):

    username: str | None
    age: int | None
    city: str | None
    country: str | None
    about_user: str | None
    user_habits: list | None


class UpdateProfile(BaseModel):
    username: Optional[str] = Field(None)
    age: Optional[int] = Field(None)
    city: Optional[str] = Field(None)
    country: Optional[str] = Field(None)
    about_user: Optional[str] = Field(None)
    user_habits: Optional[List[str]] = Field(None)

class EditProfile(BaseModel):
    profile_img: UploadFile | None = None
    username: str | None = None
    email: str | None = None
    # password: str | None = None

class Hobbies(BaseModel):
    name: str
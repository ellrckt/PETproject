from pydantic import BaseModel
from fastapi import UploadFile


class Profile(BaseModel):

    profile_img: UploadFile | None = None
    username: str
    email: str


class EditProfile(BaseModel):
    profile_img: UploadFile | None = None
    username: str | None = None
    email: str | None = None
    # password: str | None = None
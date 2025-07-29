from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter
from db.db import db_helper
from contextlib import asynccontextmanager
from fastapi.responses import ORJSONResponse
import bcrypt

from routers.user import router as user_router
from routers.user_registration import router as user_registration_router
from routers.login import router as login_router
# from routers.profiles import profiles as profile_router

from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from start_app import start_app

app = start_app(create_custom_static_urls=True)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(profile_router)
app.include_router(user_router)
app.include_router(user_registration_router)
app.include_router(login_router)

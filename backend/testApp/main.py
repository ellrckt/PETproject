from fastapi import FastAPI
from fastapi import APIRouter
from db.db import db_helper
from contextlib import asynccontextmanager
from fastapi.responses import ORJSONResponse
import bcrypt
from routers.user import router as user_router
from routers.user_registration import router as user_registration_router
from routers.login import router as login_router
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    # lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(user_registration_router)
app.include_router(login_router)


from routers.user import router as user_router
from routers.auth import registration_router as user_registration_router, login_router
from routers.profiles import router as profile_router
from routers.location import router as location_router

from fastapi.middleware.cors import CORSMiddleware
from start_app import start_app

app = start_app(create_custom_static_urls=True)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
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
app.include_router(profile_router)
app.include_router(location_router)

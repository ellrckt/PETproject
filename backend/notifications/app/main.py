from fastapi import FastAPI
from notifications.router import router as notifications_router

app = FastAPI(title="Notification Service")
app.include_router(notifications_router)

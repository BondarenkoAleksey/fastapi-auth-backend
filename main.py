from fastapi import FastAPI
from src.routers import user

app = FastAPI(title="User Authentication API")

app.include_router(user.router, prefix="/api")

from fastapi import APIRouter
from . import auth
from . import upload
from . import posts
from .assistant.router import router as assistant_router

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(upload.router)
api_router.include_router(posts.router)
api_router.include_router(assistant_router)

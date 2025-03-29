from fastapi import APIRouter
from . import auth
from . import upload
from . import posts

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(upload.router)
api_router.include_router(posts.router)

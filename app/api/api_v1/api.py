from fastapi import APIRouter

from api.api_v1.endpoints import prompted_inpainting_inference, users, login

api_router = APIRouter()
api_router.include_router(prompted_inpainting_inference.router, prefix="/inference", tags=["prompted_inpainting"])
# User login diabled as part of prototype
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(login.router, tags=["login"])
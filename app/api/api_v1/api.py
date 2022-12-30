from fastapi import APIRouter

from api.api_v1.endpoints import prompted_inpainting_inference, users

api_router = APIRouter()
api_router.include_router(prompted_inpainting_inference.router, prefix="/inference", tags=["prompted_inpainting"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

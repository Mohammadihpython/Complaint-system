from  fastapi import APIRouter
from resources import auth, complaint
api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(complaint.router)

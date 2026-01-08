from fastapi import APIRouter

from app.adapters.api.routes.domain_info import router as domain_info_router
from app.adapters.api.routes.utils import router as utils_router

api_router = APIRouter(prefix="/api")
api_router.include_router(utils_router)
api_router.include_router(domain_info_router)

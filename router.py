from fastapi import APIRouter
from api.servers.views import router as server_router
from api.auth.views import router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix='/auth', tags=['Auth'])
router.include_router(server_router, prefix='/servers', tags=['Servers'])
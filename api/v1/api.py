from fastapi import APIRouter

from api.v1.endpoints import artigos, usuario

api_router = APIRouter()

api_router.include_router(artigos.router, prefix='/artigos', tags=['artigos'])
api_router.include_router(usuario.router, prefix='/usuarios', tags=['usuarios'])
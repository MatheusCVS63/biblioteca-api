"""
Agregador de rotas da versao 1 da API.

Reunir as rotas em um unico roteador por versao (v1) e uma boa pratica de
organizacao: se no futuro a API ganhar uma v2, ela pode ser criada sem
afetar a v1 ja existente.
"""

from fastapi import APIRouter

from api.v1.endpoints import livro

api_router = APIRouter()
api_router.include_router(livro.router, prefix="/livros", tags=["livros"])

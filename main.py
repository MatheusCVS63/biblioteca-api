"""
Ponto de entrada da aplicacao.

Cria a instancia do FastAPI, registra as rotas da versao 1, configura a
politica de CORS e garante que as tabelas existam ao iniciar.

Para executar:
    uvicorn main:app --reload
A documentacao interativa (Swagger) fica disponivel em /docs.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import engine
from api.v1.api import api_router

# Importa o modelo para que o SQLAlchemy conheca a tabela antes de cria-la.
from models.livro_model import Livro  # noqa: F401

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

# Cria as tabelas no banco (caso ainda nao existam) quando a aplicacao sobe.
settings.DBBaseModel.metadata.create_all(bind=engine)

# -----------------------------------------------------------------------------
# Configuracao de CORS
#
# O CORS controla quais origens (site front-end em outro dominio/porta) podem
# consumir esta API a partir do navegador. Como o foco do trabalho e a API e
# nao ha um front-end fixo, liberamos apenas origens de desenvolvimento local
# tipicas. Em producao, bastaria trocar a lista por dominios reais.
#
# Optamos por listar origens explicitas (em vez de "*") para seguir a boa
# pratica de liberar somente o necessario.
# -----------------------------------------------------------------------------
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", settings.API_KEY_NAME],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["raiz"])
def raiz():
    """Rota simples para verificar rapidamente se a API esta no ar."""
    return {
        "aplicacao": settings.API_TITLE,
        "versao": settings.API_VERSION,
        "documentacao": "/docs",
    }

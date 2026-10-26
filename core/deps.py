"""
Dependencias reutilizaveis dos endpoints.

O FastAPI usa "injecao de dependencia": funcoes declaradas aqui sao passadas
como parametro das rotas e o proprio framework se encarrega de executa-las.
Usamos isso para abrir/fechar a sessao do banco e para validar a chave de API.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from core.config import settings
from core.database import SessionLocal

# Abre uma sessao de banco por requisicao e garante o fechamento no final.


def get_session():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Define que a chave deve chegar no cabecalho X-API-Key.
# auto_error=False faz o FastAPI nao lancar erro sozinho; tratamos abaixo
# para devolver uma mensagem mais clara.
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header)) -> str:
    """Valida a chave de API enviada no cabecalho.

    Retorna a propria chave quando valida. Caso contrario, interrompe a
    requisicao com 401 (nao autenticado), que e o codigo adequado quando
    nao ha credencial valida.
    """
    if api_key == settings.API_KEY:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Chave de API ausente ou invalida. Envie o cabecalho X-API-Key.",
    )

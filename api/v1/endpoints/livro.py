"""
Endpoints (rotas) do recurso Livro.

Implementa o CRUD completo sobre o recurso principal da API:
  - GET    /livros            -> lista a colecao (com filtros opcionais)
  - GET    /livros/{id}       -> consulta um livro especifico
  - POST   /livros            -> cria um novo livro          (protegido)
  - PATCH  /livros/{id}       -> atualiza parcialmente       (protegido)
  - DELETE /livros/{id}       -> remove um livro             (protegido)

Escolhemos PATCH (e nao PUT) para a atualizacao porque, no uso real da
aplicacao, normalmente alteramos apenas alguns campos (por exemplo, marcar
um livro como lido). O PATCH representa atualizacao parcial, evitando que o
cliente precise reenviar o recurso inteiro a cada alteracao.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.deps import get_session, get_api_key
from models.livro_model import Livro
from schemas.livro_schema import LivroCreate, LivroUpdate, LivroResponse

router = APIRouter()


@router.get("/", response_model=List[LivroResponse], status_code=status.HTTP_200_OK)
def listar_livros(
    autor: Optional[str] = Query(default=None, description="Filtra por parte do nome do autor"),
    lido: Optional[bool] = Query(default=None, description="Filtra por status de leitura"),
    db: Session = Depends(get_session),
):
    """Lista todos os livros. Aceita filtros opcionais por autor e por status de leitura."""
    query = db.query(Livro)

    if autor is not None:
        # ilike faz a busca sem diferenciar maiusculas/minusculas
        query = query.filter(Livro.autor.ilike(f"%{autor}%"))
    if lido is not None:
        query = query.filter(Livro.lido == lido)

    return query.order_by(Livro.id).all()


@router.get("/{livro_id}", response_model=LivroResponse, status_code=status.HTTP_200_OK)
def consultar_livro(livro_id: int, db: Session = Depends(get_session)):
    """Consulta um unico livro pelo seu identificador."""
    livro = db.query(Livro).filter(Livro.id == livro_id).first()

    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado.",
        )
    return livro


@router.post(
    "/",
    response_model=LivroResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_api_key)],
)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_session)):
    """Cria um novo livro. Endpoint protegido por chave de API."""
    novo_livro = Livro(
        titulo=livro.titulo,
        autor=livro.autor,
        ano_publicacao=livro.ano_publicacao,
        genero=livro.genero,
        lido=livro.lido,
    )

    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)  # recarrega o objeto para trazer o id e a data gerados
    return novo_livro


@router.patch(
    "/{livro_id}",
    response_model=LivroResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_api_key)],
)
def atualizar_livro(livro_id: int, dados: LivroUpdate, db: Session = Depends(get_session)):
    """Atualiza parcialmente um livro existente. Endpoint protegido por chave de API."""
    livro = db.query(Livro).filter(Livro.id == livro_id).first()

    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado.",
        )

    # exclude_unset=True pega apenas os campos que o cliente realmente enviou,
    # preservando os demais valores ja existentes.
    atualizacoes = dados.model_dump(exclude_unset=True)
    for campo, valor in atualizacoes.items():
        setattr(livro, campo, valor)

    db.commit()
    db.refresh(livro)
    return livro


@router.delete(
    "/{livro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_api_key)],
)
def remover_livro(livro_id: int, db: Session = Depends(get_session)):
    """Remove um livro existente. Endpoint protegido por chave de API."""
    livro = db.query(Livro).filter(Livro.id == livro_id).first()

    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado.",
        )

    db.delete(livro)
    db.commit()
    # 204 No Content: operacao concluida, nada a retornar no corpo.
    return None

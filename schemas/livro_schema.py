"""
Schemas (Pydantic) do recurso Livro.

Enquanto o modelo representa a tabela no banco, os schemas representam os
dados que entram e saem pela API. O Pydantic valida automaticamente os dados
recebidos e serializa as respostas em JSON. Separar os schemas por operacao
evita, por exemplo, que o cliente tente definir o 'id' na criacao.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LivroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255, description="Titulo do livro")
    autor: str = Field(..., min_length=1, max_length=255, description="Nome do autor")
    ano_publicacao: Optional[int] = Field(
        default=None, ge=0, le=2100, description="Ano de publicacao"
    )
    genero: Optional[str] = Field(default=None, max_length=100)
    lido: bool = Field(default=False, description="Indica se o livro ja foi lido")


class LivroCreate(LivroBase):
    """Dados aceitos na criacao (POST). Herda todos os campos de LivroBase."""
    pass


class LivroUpdate(BaseModel):
    """Dados aceitos na atualizacao parcial (PATCH).

    Todos os campos sao opcionais: o cliente envia apenas o que quer alterar.
    """
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=255)
    autor: Optional[str] = Field(default=None, min_length=1, max_length=255)
    ano_publicacao: Optional[int] = Field(default=None, ge=0, le=2100)
    genero: Optional[str] = Field(default=None, max_length=100)
    lido: Optional[bool] = None


class LivroResponse(LivroBase):
    """Formato devolvido pela API. Inclui os campos gerados pelo servidor."""
    id: int
    criado_em: datetime

    class Config:
        # Permite que o Pydantic leia os dados direto de um objeto ORM
        # (instancia de Livro), e nao apenas de um dicionario.
        from_attributes = True

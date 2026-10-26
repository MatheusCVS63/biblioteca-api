"""
Modelo de dados (ORM) do recurso Livro.

Esta classe e o mapeamento objeto-relacional: cada atributo da classe vira
uma coluna na tabela 'livros', e cada objeto Livro representa uma linha dessa
tabela. O SQLAlchemy cuida de traduzir isso para comandos SQL.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from core.config import settings


class Livro(settings.DBBaseModel):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    ano_publicacao = Column(Integer, nullable=True)
    genero = Column(String(100), nullable=True)
    lido = Column(Boolean, default=False, nullable=False)
    criado_em = Column(DateTime, default=datetime.now, nullable=False)

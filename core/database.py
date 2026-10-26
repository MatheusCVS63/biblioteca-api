"""
Camada de conexao com o banco de dados.

Cria o engine do SQLAlchemy (que gerencia a conexao com o banco) e a fabrica
de sessoes (SessionLocal). A sessao e o objeto que usamos para consultar e
gravar dados usando a abordagem de ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

# O connect_args com check_same_thread=False e necessario apenas para o SQLite,
# porque por padrao ele nao permite que a mesma conexao seja usada por threads
# diferentes, e o servidor web pode atender requisicoes em threads distintas.
connect_args = {"check_same_thread": False} if settings.DB_URL.startswith("sqlite") else {}

engine = create_engine(settings.DB_URL, connect_args=connect_args)

# autocommit=False e autoflush=False dao controle explicito sobre quando os
# dados sao enviados ao banco (via commit), que e a forma recomendada.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

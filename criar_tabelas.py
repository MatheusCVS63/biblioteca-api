"""
Script utilitario para criar as tabelas do banco de dados.

Rodar este arquivo cria o arquivo do banco (SQLite) e a tabela 'livros' a
partir dos modelos do SQLAlchemy. Nao e obrigatorio executa-lo separadamente,
pois o main.py tambem cria as tabelas ao iniciar, mas ele e util para
preparar o banco antes de rodar a aplicacao ou para recriar a estrutura.

Uso:
    python criar_tabelas.py
"""

from core.config import settings
from core.database import engine

# Importar o modelo registra a tabela nos metadados do SQLAlchemy.
from models.livro_model import Livro  # noqa: F401


def criar():
    settings.DBBaseModel.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso em:", settings.DB_URL)


if __name__ == "__main__":
    criar()

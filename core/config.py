"""
Configurações gerais da aplicação.

Aqui ficam os valores comuns usados em vários pontos do projeto, como a URL
do banco de dados, a Base declarativa do SQLAlchemy e a chave de API usada
na autenticacao. Os valores sensiveis sao lidos de variaveis de ambiente,
com um valor padrao apenas para facilitar a execucao em ambiente local.
"""

import os

from sqlalchemy.orm import declarative_base


class Settings:
    # Titulo que aparece na documentacao automatica (Swagger) do FastAPI
    API_TITLE: str = "API Biblioteca Pessoal"
    API_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # String de conexao com o banco. Usamos SQLite porque ele e nativo do
    # Python e nao exige a instalacao de um driver ou servidor separado,
    # facilitando a reproducao do projeto por quem for avaliar.
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./biblioteca.db")

    # Base declarativa do SQLAlchemy. Todos os modelos (tabelas) herdam dela.
    DBBaseModel = declarative_base()

    # Chave de API usada para proteger endpoints de escrita.
    # Em producao deve vir de uma variavel de ambiente e nunca ir para o
    # repositorio. O valor padrao abaixo serve apenas para testes locais.
    API_KEY: str = os.getenv("API_KEY", "biblioteca-chave-local")

    # Nome do cabecalho HTTP onde a chave de API deve ser enviada.
    API_KEY_NAME: str = "X-API-Key"


settings = Settings()

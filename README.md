# API Biblioteca Pessoal

API Web para gerenciar uma biblioteca pessoal de livros. Permite cadastrar,
consultar, atualizar e remover livros, além de filtrar por autor e por status
de leitura.

Projeto desenvolvido para a disciplina de **Arquitetura e Desenvolvimento de
APIs** (ADS).

- **Aluno:** Matheus Cavalcanti e Sousa
- **RU:** 5482872

---

## Descrição do problema

Quem gosta de ler costuma perder o controle dos livros que já leu, dos que
ainda quer ler e de quem escreveu cada um. Esta API resolve isso oferecendo
um cadastro simples de livros, com um recurso principal (`livros`) e operações
completas de CRUD, podendo servir de back-end para um aplicativo web ou mobile
de controle de leituras.

## Tecnologias utilizadas

| Tecnologia | Função |
|------------|--------|
| Python 3 | Linguagem de programação |
| FastAPI | Framework web para construção da API |
| SQLAlchemy | ORM (mapeamento objeto-relacional) e acesso ao banco |
| Pydantic | Validação e serialização dos dados (schemas) |
| SQLite | Banco de dados relacional (persistência) |
| Uvicorn | Servidor ASGI que executa a aplicação |

## Pré-requisitos

- Python 3.10 ou superior instalado.

## Instalação

No diretório do projeto (`biblioteca-api`):

```bash
# 1. Criar o ambiente virtual
python -m venv venv

# 2. Ativar o ambiente virtual
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt
```

## Configuração

A aplicação funciona com os valores padrão sem nenhuma configuração extra.
Opcionalmente, você pode criar um arquivo `.env` (baseado no `.env.example`)
para alterar a URL do banco ou a chave de API:

```
DB_URL=sqlite:///./biblioteca.db
API_KEY=biblioteca-chave-local
```

> As variáveis acima são lidas do ambiente. O arquivo `.env` não deve ser
> versionado (já está no `.gitignore`), para não expor segredos.

## Banco de dados

O projeto usa **SQLite**, que é nativo do Python e não exige instalação de
servidor. O arquivo do banco (`biblioteca.db`) é criado automaticamente na
primeira execução. Para criar/recriar a estrutura manualmente:

```bash
python criar_tabelas.py
```

## Como executar

```bash
uvicorn main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.

## Documentação (Swagger)

Com a aplicação em execução, a documentação interativa gerada automaticamente
pelo FastAPI fica em:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI (JSON): http://127.0.0.1:8000/openapi.json

Pela interface do Swagger é possível testar todos os endpoints. Para os
endpoints protegidos, use o botão **Authorize** e informe a chave de API.

## Autenticação

Os endpoints de escrita (POST, PATCH e DELETE) são protegidos por **API Key**.
A chave deve ser enviada no cabeçalho HTTP:

```
X-API-Key: biblioteca-chave-local
```

Requisições de leitura (GET) são públicas. Requisições de escrita sem a chave
correta recebem `401 Unauthorized`.

## Resumo dos endpoints

Prefixo base: `/api/v1`

| Método | Endpoint | Finalidade | Protegido |
|--------|----------|------------|-----------|
| GET | `/livros` | Lista os livros (filtros opcionais) | Não |
| GET | `/livros/{id}` | Consulta um livro específico | Não |
| POST | `/livros` | Cria um novo livro | Sim |
| PATCH | `/livros/{id}` | Atualiza parcialmente um livro | Sim |
| DELETE | `/livros/{id}` | Remove um livro | Sim |

Filtros do `GET /livros`:
- `?autor=<texto>` — filtra por parte do nome do autor.
- `?lido=true|false` — filtra pelo status de leitura.

## Exemplo de requisição

Criar um livro (endpoint protegido):

```bash
curl -X POST http://127.0.0.1:8000/api/v1/livros \
  -H "Content-Type: application/json" \
  -H "X-API-Key: biblioteca-chave-local" \
  -d "{\"titulo\": \"Dom Casmurro\", \"autor\": \"Machado de Assis\", \"ano_publicacao\": 1899, \"genero\": \"Romance\"}"
```

Resposta (`201 Created`):

```json
{
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano_publicacao": 1899,
  "genero": "Romance",
  "lido": false,
  "id": 1,
  "criado_em": "2026-01-01T12:00:00"
}
```

Listar apenas livros já lidos:

```bash
curl "http://127.0.0.1:8000/api/v1/livros?lido=true"
```

## Estrutura do projeto

```
biblioteca-api/
├── api/
│   └── v1/
│       ├── api.py            # agrega as rotas da versão 1
│       └── endpoints/
│           └── livro.py      # endpoints (CRUD) do recurso livro
├── core/
│   ├── config.py             # configurações (banco, chave de API)
│   ├── database.py           # engine e sessão do SQLAlchemy
│   └── deps.py               # dependências (sessão de banco, API Key)
├── models/
│   └── livro_model.py        # modelo ORM (tabela livros)
├── schemas/
│   └── livro_schema.py       # schemas Pydantic (entrada/saída)
├── criar_tabelas.py          # cria as tabelas no banco
├── main.py                   # ponto de entrada + CORS
├── requirements.txt          # dependências
├── .env.example              # exemplo de variáveis de ambiente
└── .gitignore
```

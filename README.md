# Sistema de Gestão de Garantias

API REST para gestão de suppliers, transações e analytics desenvolvida com FastAPI.

## Requisitos

- Python 3.8+
- PostgreSQL
- pip (gerenciador de pacotes Python)

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd teste_tecnico_backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
- Copie o arquivo `.env.example` para `.env`
- Edite o arquivo `.env` com suas configurações

5. Configure o banco de dados:
```bash
# Inicialize as migrações
alembic upgrade head
```

## Executando a Aplicação

1. Inicie o servidor de desenvolvimento:
```bash
uvicorn app.main:app --reload
```

2. Acesse a documentação da API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estrutura do Projeto

```
app/
├── api/            # Rotas da API
├── core/           # Configurações centrais
├── db/             # Configuração do banco de dados
├── models/         # Modelos SQLAlchemy
├── schemas/        # Schemas Pydantic
├── services/       # Lógica de negócios
└── tests/          # Testes
```

## Funcionalidades

- CRUD completo para suppliers e transações
- Sistema de autenticação JWT
- Endpoints analíticos
- Documentação automática via Swagger/OpenAPI
- Testes automatizados

## Endpoints Principais

- `/api/v1/suppliers/`: Gerenciamento de fornecedores
- `/api/v1/warranties/`: Gerenciamento de garantias
- `/api/v1/analytics/`: Endpoints analíticos
- `/api/v1/auth/`: Autenticação e autorização

## Segurança

- Autenticação via JWT
- Dados sensíveis criptografados
- Configuração CORS
- Validação de dados via Pydantic

## Testes

Execute os testes com:
```bash
pytest
``` 
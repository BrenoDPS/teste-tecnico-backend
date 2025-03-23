# Sistema de Gestão de Garantias

API REST para gestão de suppliers, transações e analytics desenvolvida com FastAPI.

## Requisitos

- Python 3.8+
- FastAPI
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
alembic/            # Migrações no banco de dados feitas com Alembic
app/
├── api/            # Rotas da API
├── core/           # Configurações centrais
├── db/             # Configuração do banco de dados
├── models/         # Modelos SQLAlchemy
├── schemas/        # Schemas Pydantic
└── services/       # Lógica de negócios
tests/              # Testes
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

### Autenticação e Autorização

O sistema utiliza um mecanismo robusto de autenticação e autorização baseado em JWT (JSON Web Tokens):

1. **Registro e Login**:
   - Endpoint `/api/v1/auth/register` para criar novos usuários
   - Endpoint `/api/v1/auth/token` para autenticação e geração de token
   - Endpoint `/api/v1/auth/logout` para invalidar o token atual
   - Senhas são armazenadas com hash usando bcrypt

2. **JWT (JSON Web Tokens)**:
   - Tokens são assinados com algoritmo HS256
   - Tempo de expiração configurável (padrão: 30 minutos)
   - Payload inclui informações do usuário e claims padrão (exp, sub)
   - Validação automática de tokens expirados

3. **Proteção de Rotas**:
   - Middleware de autenticação via `get_current_active_user`
   - Verificação de tokens em todas as rotas protegidas
   - Validação de usuários ativos
   - Suporte a diferentes níveis de acesso (usuário normal/superusuário)

### Proteção de Dados

1. **Criptografia**:
   - Senhas: Hash usando bcrypt com salt automático
   - Dados sensíveis: Criptografia em nível de banco de dados
   - Variáveis de ambiente para chaves secretas

2. **CORS (Cross-Origin Resource Sharing)**:
   - Configuração granular de origens permitidas
   - Controle de métodos HTTP permitidos
   - Gerenciamento de headers personalizados
   - Suporte a credenciais em requisições cross-origin

3. **Validação de Dados**:
   - Schemas Pydantic para validação de entrada
   - Sanitização automática de dados
   - Tipagem forte em todas as operações
   - Prevenção contra injeção SQL via SQLAlchemy

## Testes

Execute os testes com:
```bash
pytest
``` 
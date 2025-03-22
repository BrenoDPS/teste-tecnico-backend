from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, bulk_operations, suppliers

app = FastAPI(
    title="Sistema de Gestão de Garantias",
    description="API para gestão de suppliers, transações e analytics",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers
app.include_router(auth.router)
app.include_router(bulk_operations.router)
app.include_router(suppliers.router)

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo ao Sistema de Gestão de Garantias",
        "docs": "/docs",
        "redoc": "/redoc"
    } 
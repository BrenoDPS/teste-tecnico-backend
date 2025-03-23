from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, bulk_operations, suppliers
from .core.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
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
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(bulk_operations.router)
app.include_router(suppliers.router)

@app.get("/")
async def root():
    return {
        "message": f"Bem-vindo ao {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    } 
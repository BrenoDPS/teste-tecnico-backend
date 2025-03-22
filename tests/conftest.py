import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.database import Base, get_db
from app.models.auth import User
from app.core.security import get_password_hash

# Criar banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    # Criar as tabelas no banco de teste
    Base.metadata.create_all(bind=engine)
    
    # Criar um usuário de teste
    db = TestingSessionLocal()
    test_user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpass"),
        is_active=True
    )
    db.add(test_user)
    db.commit()
    
    try:
        yield db
    finally:
        db.close()
        # Limpar as tabelas após os testes
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db] 
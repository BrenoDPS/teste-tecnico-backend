from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import get_password_hash
from app.db.database import Base, get_db
from app.main import app
from app.models.auth import User
from app.models.models import DimSupplier

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
        is_active=True,
    )
    db.add(test_user)
    db.commit()

    try:
        yield db
    except Exception as e:
        print(f"Erro durante o teste: {e}")
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


@pytest.fixture
def auth_headers(client: TestClient, db: Session):
    """Fixture que fornece headers de autenticação para os testes"""
    # Criar usuário de teste se não existir
    username = "testuser"
    password = "testpass"

    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(
            username=username,
            hashed_password=get_password_hash(password),
            is_active=True,
        )
        db.add(user)
        db.commit()

    # Obter token
    response = client.post(
        "/api/v1/auth/token", data={"username": username, "password": password}
    )
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_supplier(db: Session):
    """Fixture que cria um fornecedor de teste"""
    supplier = DimSupplier(
        supplier_name="Fornecedor Teste", _encrypted_cpf="123.456.789-00"
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    # Armazenar o ID antes de retornar
    supplier_id = supplier.supplier_id

    yield supplier

    try:
        # Cleanup usando o ID armazenado
        db.query(DimSupplier).filter_by(supplier_id=supplier_id).delete()
        db.commit()
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        db.rollback()

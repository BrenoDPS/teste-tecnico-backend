import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.models import DimSupplier


@pytest.fixture
def test_supplier():
    return {"supplier_name": "Fornecedor Teste", "location_id": 1}


@pytest.fixture
def auth_headers():
    access_token = create_access_token({"sub": "testuser"})
    return {"Authorization": f"Bearer {access_token}"}


def test_create_supplier(client: TestClient, test_supplier: dict, auth_headers: dict):
    response = client.post(
        "/api/v1/suppliers/", json=test_supplier, headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["supplier_name"] == test_supplier["supplier_name"]
    assert data["location_id"] == test_supplier["location_id"]
    assert "supplier_id" in data


def test_read_supplier(
    client: TestClient, test_supplier: dict, auth_headers: dict, db: Session
):
    # Criar um fornecedor para teste
    db_supplier = DimSupplier(**test_supplier)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    response = client.get(
        f"/api/v1/suppliers/{db_supplier.supplier_id}", headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["supplier_name"] == test_supplier["supplier_name"]
    assert data["location_id"] == test_supplier["location_id"]


def test_list_suppliers(
    client: TestClient, test_supplier: dict, auth_headers: dict, db: Session
):
    # Criar alguns fornecedores para teste
    db_supplier1 = DimSupplier(**test_supplier)
    db_supplier2 = DimSupplier(supplier_name="Another Supplier", location_id=2)
    db.add(db_supplier1)
    db.add(db_supplier2)
    db.commit()

    response = client.get("/api/v1/suppliers/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(s["supplier_name"] == test_supplier["supplier_name"] for s in data)


def test_update_supplier(
    client: TestClient, test_supplier: dict, auth_headers: dict, db: Session
):
    # Criar um fornecedor para teste
    db_supplier = DimSupplier(**test_supplier)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    updated_data = {"supplier_name": "Updated Supplier", "location_id": 3}
    response = client.put(
        f"/api/v1/suppliers/{db_supplier.supplier_id}",
        json=updated_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["supplier_name"] == updated_data["supplier_name"]
    assert data["location_id"] == updated_data["location_id"]


def test_delete_supplier(
    client: TestClient, test_supplier: dict, auth_headers: dict, db: Session
):
    # Criar um fornecedor para teste
    db_supplier = DimSupplier(**test_supplier)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    response = client.delete(
        f"/api/v1/suppliers/{db_supplier.supplier_id}", headers=auth_headers
    )
    assert response.status_code == 204

    # Verificar se foi realmente deletado
    response = client.get(
        f"/api/v1/suppliers/{db_supplier.supplier_id}", headers=auth_headers
    )
    assert response.status_code == 404


def test_create_supplier_unauthorized(client: TestClient, test_supplier: dict):
    response = client.post("/api/v1/suppliers/", json=test_supplier)
    assert response.status_code == 401


def test_read_supplier_not_found(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/suppliers/999999", headers=auth_headers)
    assert response.status_code == 404

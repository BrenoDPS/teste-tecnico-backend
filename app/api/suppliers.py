from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..db.database import get_db
from ..models.models import DimSupplier
from ..schemas.base import Supplier, SupplierCreate

router = APIRouter(prefix="/api/v1/suppliers", tags=["suppliers"])


@router.get("/", response_model=List[Supplier])
async def list_suppliers(
    name: str | None = None,
    location_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Lista todos os fornecedores com opção de filtro por nome e localização.
    Requer autenticação.
    """
    query = db.query(DimSupplier)

    if name:
        query = query.filter(DimSupplier.supplier_name.ilike(f"%{name}%"))
    if location_id:
        query = query.filter(DimSupplier.location_id == location_id)

    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=Supplier, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Cria um novo fornecedor.
    Requer autenticação.
    """
    db_supplier = DimSupplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@router.get("/{supplier_id}", response_model=Supplier)
async def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Retorna um fornecedor específico por ID.
    Requer autenticação.
    """
    supplier = (
        db.query(DimSupplier).filter(DimSupplier.supplier_id == supplier_id).first()
    )
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado"
        )
    return supplier


@router.put("/{supplier_id}", response_model=Supplier)
async def update_supplier(
    supplier_id: int,
    supplier_update: SupplierCreate,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Atualiza um fornecedor existente.
    Requer autenticação.
    """
    db_supplier = (
        db.query(DimSupplier).filter(DimSupplier.supplier_id == supplier_id).first()
    )
    if not db_supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado"
        )

    for key, value in supplier_update.model_dump().items():
        setattr(db_supplier, key, value)

    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Remove um fornecedor.
    Requer autenticação.
    """
    db_supplier = (
        db.query(DimSupplier).filter(DimSupplier.supplier_id == supplier_id).first()
    )
    if not db_supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado"
        )

    db.delete(db_supplier)
    db.commit()
    return None

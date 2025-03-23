from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..db.database import get_db
from ..models.models import DimPurchances
from ..schemas.base import Purchance, PurchanceCreate

router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


@router.get("/", response_model=List[Purchance])
async def list_transactions(
    purchance_type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    part_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Lista todas as transações com opções de filtro.
    Requer autenticação.
    """
    query = db.query(DimPurchances)

    if purchance_type:
        query = query.filter(DimPurchances.purchance_type == purchance_type)
    if start_date and end_date:
        query = query.filter(DimPurchances.purchance_date.between(start_date, end_date))
    if part_id:
        query = query.filter(DimPurchances.part_id == part_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{purchance_id}", response_model=Purchance)
async def get_transaction(
    purchance_id: int,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Retorna uma transação específica pelo ID.
    Requer autenticação.
    """
    transaction = (
        db.query(DimPurchances)
        .filter(DimPurchances.purchance_id == purchance_id)
        .first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
        )
    return transaction


@router.post("/", response_model=Purchance)
async def create_transaction(
    transaction: PurchanceCreate,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Cria uma nova transação.
    Requer autenticação.
    """
    db_transaction = DimPurchances(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.put("/{purchance_id}", response_model=Purchance)
async def update_transaction(
    purchance_id: int,
    transaction: PurchanceCreate,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Atualiza uma transação existente.
    Requer autenticação.
    """
    db_transaction = (
        db.query(DimPurchances)
        .filter(DimPurchances.purchance_id == purchance_id)
        .first()
    )
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
        )

    for key, value in transaction.model_dump().items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.delete("/{purchance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    purchance_id: int,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user),
):
    """
    Remove uma transação.
    Requer autenticação.
    """
    db_transaction = (
        db.query(DimPurchances)
        .filter(DimPurchances.purchance_id == purchance_id)
        .first()
    )
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
        )

    db.delete(db_transaction)
    db.commit()

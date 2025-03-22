from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..db.database import get_db
from ..services.bulk_operations import BulkOperationsService
from ..schemas.bulk_operations import (
    BulkCreateVehicle, BulkCreatePart,
    DateRangeFilter, SupplierFilter, TransactionFilter
)
from ..core.security import get_current_active_user

router = APIRouter(prefix="/api/v1", tags=["bulk_operations"])

@router.post("/vehicles/bulk", response_model=List[Dict[str, Any]])
async def bulk_create_vehicles(
    vehicles: BulkCreateVehicle,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Cria múltiplos veículos em uma única operação.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    return await service.bulk_create_vehicles(vehicles)

@router.post("/parts/bulk", response_model=List[Dict[str, Any]])
async def bulk_create_parts(
    parts: BulkCreatePart,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Cria múltiplas peças em uma única operação.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    return await service.bulk_create_parts(parts)

@router.get("/analytics/supplier-sales")
async def get_supplier_sales_analytics(
    name: str | None = None,
    location_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna análise de vendas por fornecedor.
    Permite filtrar por nome, localização e período.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    supplier_filter = SupplierFilter(name=name, location_id=location_id)
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date) if start_date and end_date else None
    return await service.get_supplier_sales_analytics(supplier_filter, date_range)

@router.get("/analytics/warranty-by-model")
async def get_warranty_analytics_by_model(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna análise de garantias por modelo de veículo.
    Permite filtrar por período.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date) if start_date and end_date else None
    return await service.get_warranty_analytics_by_model(date_range)

@router.get("/analytics/transactions")
async def get_transaction_analytics(
    transaction_type: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    supplier_id: int | None = None,
    model: str | None = None,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna análise de transações (compras e garantias).
    Permite filtrar por tipo, período, fornecedor e modelo.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date) if start_date and end_date else None
    transaction_filter = TransactionFilter(
        transaction_type=transaction_type,
        date_range=date_range,
        supplier_id=supplier_id,
        model=model
    )
    return await service.get_transaction_analytics(transaction_filter) 
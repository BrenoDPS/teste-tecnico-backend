from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..db.database import get_db
from ..services.bulk_operations import BulkOperationsService
from ..schemas.bulk_operations import (
    BulkCreateVehicle, BulkCreatePart, BulkCreateSupplier,
    BulkCreatePurchance, BulkCreateWarranty,
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

@router.post("/suppliers/bulk", response_model=List[Dict[str, Any]])
async def bulk_create_suppliers(
    suppliers: BulkCreateSupplier,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Cria múltiplos fornecedores em uma única operação.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    return await service.bulk_create_suppliers(suppliers)

@router.post("/purchances/bulk", response_model=List[Dict[str, Any]])
async def bulk_create_purchances(
    purchances: BulkCreatePurchance,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):    
    """
    Cria múltiplas transações em uma única operação.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    return await service.bulk_create_purchances(purchances)


@router.post("/warranties/bulk", response_model=List[Dict[str, Any]])
async def bulk_create_warranties(
    warranties: BulkCreateWarranty,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Cria múltiplas garantias em uma única operação.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    return await service.bulk_create_warranties(warranties)

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
    start_date: str | None = None,
    end_date: str | None = None,
    purchance_type: str | None = None,
    part_id: int | None = None,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna análise de transações com opções de filtro por data, tipo e peça.
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    filter = TransactionFilter(
        start_date=start_date,
        end_date=end_date,
        purchance_type=purchance_type,
        part_id=part_id
    ) if start_date and end_date else None
    return await service.get_transaction_analytics(filter)

@router.get("/analytics/supplier-transactions")
async def get_average_transactions_by_supplier(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna análise de transações por fornecedor, incluindo:
    - Total de transações
    - Média de compras e garantias
    - Proporção entre garantias e compras
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date) if start_date and end_date else None
    return await service.get_average_transactions_by_supplier(date_range)

@router.get("/analytics/model-transactions")
async def get_transactions_by_model(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna análise de transações por modelo de veículo, incluindo:
    - Contagem de garantias
    - Número de peças únicas
    - Número de fornecedores únicos
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date) if start_date and end_date else None
    return await service.get_transactions_by_model(date_range)

@router.get("/analytics/part-performance")
async def get_part_performance_analytics(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_active_user)
):
    """
    Retorna análise de desempenho das peças, incluindo:
    - Contagem de garantias por peça
    - Tipos de falhas por peça
    - Agrupamento por fornecedor
    Requer autenticação.
    """
    service = BulkOperationsService(db)
    date_range = DateRangeFilter(start_date=start_date, end_date=end_date) if start_date and end_date else None
    return await service.get_part_performance_analytics(date_range)
from datetime import date
from typing import List

from pydantic import BaseModel

from .base import (
    LocationBase,
    PartBase,
    PurchanceBase,
    SupplierBase,
    VehicleBase,
    WarrantyBase,
)


class BulkCreateVehicle(BaseModel):
    vehicles: List[VehicleBase]


class BulkCreatePart(BaseModel):
    parts: List[PartBase]


class BulkCreateSupplier(BaseModel):
    suppliers: List[SupplierBase]


class BulkCreateLocation(BaseModel):
    locations: List[LocationBase]


class BulkCreatePurchance(BaseModel):
    purchances: List[PurchanceBase]


class BulkCreateWarranty(BaseModel):
    warranties: List[WarrantyBase]


# Schemas para filtros de consulta
class DateRangeFilter(BaseModel):
    start_date: date
    end_date: date


class SupplierFilter(BaseModel):
    name: str | None = None
    location_id: int | None = None


class TransactionFilter(BaseModel):
    transaction_type: str | None = None
    date_range: DateRangeFilter | None = None
    supplier_id: int | None = None
    model: str | None = None


# Schemas para respostas analíticas
class SupplierSalesAnalytics(BaseModel):
    supplier_id: int
    supplier_name: str
    total_sales: float
    parts_sold: List[dict]
    total_warranties: int


class ModelWarrantyAnalytics(BaseModel):
    model: str
    total_warranties: int
    warranty_percentage: float
    common_issues: List[dict]


class TransactionAnalytics(BaseModel):
    transaction_type: str
    average_value: float
    total_count: int
    by_model: List[dict]

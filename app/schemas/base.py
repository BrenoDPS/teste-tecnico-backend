from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Schemas para Vehicle
class VehicleBase(BaseModel):
    model: str
    prod_date: date
    year: int
    propulsion: str


class VehicleCreate(VehicleBase):
    pass


class Vehicle(VehicleBase):
    vehicle_id: int
    model_config = ConfigDict(from_attributes=True)


# Schemas para Parts
class PartBase(BaseModel):
    part_name: str
    supplier_id: int


class PartCreate(PartBase):
    pass


class Part(PartBase):
    part_id: int
    last_id_purchase: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# Schemas para Supplier
class SupplierBase(BaseModel):
    supplier_name: str
    location_id: int


class SupplierCreate(SupplierBase):
    pass


class Supplier(SupplierBase):
    supplier_id: int
    model_config = ConfigDict(from_attributes=True)


# Schemas para Location
class LocationBase(BaseModel):
    market: str
    country: str
    province: str
    city: str


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    location_id: int
    model_config = ConfigDict(from_attributes=True)


# Schemas para Purchase
class PurchanceBase(BaseModel):
    purchance_type: str
    purchance_date: date
    part_id: int


class PurchanceCreate(PurchanceBase):
    pass


class Purchance(PurchanceBase):
    purchance_id: int

    class Config:
        from_attributes = True


# Schemas para Warranty
class WarrantyBase(BaseModel):
    vehicle_id: int
    repair_date: date
    client_comment: Optional[str] = None
    tech_comment: Optional[str] = None
    part_id: int
    classifed_as: str
    location_id: int
    purchance_id: int


class WarrantyCreate(WarrantyBase):
    pass


class Warranty(WarrantyBase):
    claim_key: int
    model_config = ConfigDict(from_attributes=True)


# Schemas para respostas analíticas
class SupplierSalesReport(BaseModel):
    supplier_id: int
    supplier_name: str
    total_sales: float
    total_warranties: int


class VehicleWarrantyReport(BaseModel):
    model: str
    total_warranties: int
    warranty_percentage: float


class LocationAnalytics(BaseModel):
    location_id: int
    city: str
    total_warranties: int
    most_common_issue: str

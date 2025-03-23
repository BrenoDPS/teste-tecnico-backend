from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, case, distinct, literal
from ..models.models import DimVehicle, DimParts, DimSupplier, DimPurchances, FactWarranties
from ..schemas.bulk_operations import (
    BulkCreateVehicle, BulkCreatePart, BulkCreateSupplier,
    BulkCreatePurchance, BulkCreateWarranty,
    DateRangeFilter, SupplierFilter, TransactionFilter
)

class BulkOperationsService:
    def __init__(self, db: Session):
        self.db = db

    async def bulk_create_suppliers(self, suppliers: BulkCreateSupplier):
        db_suppliers = [DimSupplier(**supplier.model_dump()) for supplier in suppliers.suppliers]
        self.db.add_all(db_suppliers)
        self.db.commit()
        return [
            {
                "supplier_id": supplier.supplier_id,
                "supplier_name": supplier.supplier_name,
                "location_id": supplier.location_id
            }
            for supplier in db_suppliers
        ]
    
    async def bulk_create_purchances(self, purchances: BulkCreatePurchance):
        db_purchances = [DimPurchances(**purchance.model_dump()) for purchance in purchances.purchances]
        self.db.add_all(db_purchances)
        self.db.commit()
        return [
            {
                "purchance_id": purchance.purchance_id,
                "purchance_type": purchance.purchance_type,
                "purchance_date": purchance.purchance_date,
                "part_id": purchance.part_id
            }
            for purchance in db_purchances
        ]

    async def bulk_create_vehicles(self, vehicles: BulkCreateVehicle):
        db_vehicles = [DimVehicle(**vehicle.model_dump()) for vehicle in vehicles.vehicles]
        self.db.add_all(db_vehicles)
        self.db.commit()
        
        # Convertendo para dicionário antes de retornar
        return [
            {
                "vehicle_id": vehicle.vehicle_id,
                "model": vehicle.model,
                "prod_date": vehicle.prod_date,
                "year": vehicle.year,
                "propulsion": vehicle.propulsion
            }
            for vehicle in db_vehicles
        ]

    async def bulk_create_parts(self, parts: BulkCreatePart):
        db_parts = [DimParts(**part.model_dump()) for part in parts.parts]
        self.db.add_all(db_parts)
        self.db.commit()
        return [
            {
                "part_id": part.part_id,
                "part_name": part.part_name,
                "supplier_id": part.supplier_id,
                "last_id_purchase": part.last_id_purchase
            }
            for part in db_parts
        ]
    
    async def bulk_create_warranties(self, warranties: BulkCreateWarranty):
        db_warranties = [FactWarranties(**warranty.model_dump()) for warranty in warranties.warranties]
        self.db.add_all(db_warranties)
        self.db.commit()
        return [
            {
                "claim_key": warranty.claim_key,
                "vehicle_id": warranty.vehicle_id,
                "repair_date": warranty.repair_date,
                "part_id": warranty.part_id,
                "classifed_as": warranty.classifed_as,
                "location_id": warranty.location_id,
                "purchance_id": warranty.purchance_id
            }
            for warranty in db_warranties
        ]

    async def get_supplier_sales_analytics(
        self,
        supplier_filter: SupplierFilter | None = None,
        date_range: DateRangeFilter | None = None
    ):
        query = self.db.query(
            DimSupplier.supplier_id,
            DimSupplier.supplier_name,
            func.count(FactWarranties.claim_key).label('total_warranties'),
            func.count(DimPurchances.purchance_id).label('total_purchases')
        ).join(
            DimParts, DimSupplier.supplier_id == DimParts.supplier_id
        ).outerjoin(
            FactWarranties, DimParts.part_id == FactWarranties.part_id
        ).outerjoin(
            DimPurchances, DimParts.part_id == DimPurchances.part_id
        ).group_by(
            DimSupplier.supplier_id,
            DimSupplier.supplier_name
        )

        if supplier_filter:
            if supplier_filter.name:
                query = query.filter(DimSupplier.supplier_name.ilike(f"%{supplier_filter.name}%"))
            if supplier_filter.location_id:
                query = query.filter(DimSupplier.location_id == supplier_filter.location_id)

        if date_range:
            query = query.filter(
                DimPurchances.purchance_date.between(date_range.start_date, date_range.end_date)
            )

        return [
            {
                "supplier_id": row.supplier_id,
                "supplier_name": row.supplier_name,
                "total_warranties": row.total_warranties,
                "total_purchases": row.total_purchases
            }
            for row in query.all()
        ]

    async def get_warranty_analytics_by_model(
        self,
        date_range: DateRangeFilter | None = None
    ):
        query = self.db.query(
            DimVehicle.model,
            func.count(FactWarranties.claim_key).label('total_warranties'),
            func.count(func.distinct(FactWarranties.classifed_as)).label('unique_issues')
        ).join(
            FactWarranties, DimVehicle.vehicle_id == FactWarranties.vehicle_id
        ).group_by(
            DimVehicle.model
        )

        if date_range:
            query = query.filter(
                FactWarranties.repair_date.between(date_range.start_date, date_range.end_date)
            )

        return [
            {
                "model": row.model,
                "total_warranties": row.total_warranties,
                "unique_issues": row.unique_issues
            }
            for row in query.all()
        ]

    async def get_transaction_analytics(self, filter: TransactionFilter | None = None):
        query = self.db.query(
            DimPurchances.purchance_type,
            func.count(DimPurchances.purchance_id).label('total_count')
        ).group_by(DimPurchances.purchance_type)

        if filter:
            if filter.start_date and filter.end_date:
                query = query.filter(
                    DimPurchances.purchance_date.between(filter.start_date, filter.end_date)
                )
            if filter.purchance_type:
                query = query.filter(DimPurchances.purchance_type == filter.purchance_type)
            if filter.part_id:
                query = query.filter(DimPurchances.part_id == filter.part_id)

        results = query.all()
        return {
            "transactions": [
                {"type": r.purchance_type, "count": r.total_count}
                for r in results
            ]
        }
    
    async def get_average_transactions_by_supplier(self, date_range: DateRangeFilter | None = None):
        """Calcula a média de transações por fornecedor"""
        query = self.db.query(
            DimSupplier.supplier_id,
            DimSupplier.supplier_name,
            func.count(DimPurchances.purchance_id).label('total_transactions'),
            func.count(
                case(
                    (DimPurchances.purchance_type == 'COMPRA', literal(1)),
                    else_=literal(0)
                )
            ).label('total_purchases'),
            func.count(
                case(
                    (DimPurchances.purchance_type == 'GARANTIA', literal(1)),
                    else_=literal(0)
                )
            ).label('total_warranties')
        ).join(
            DimParts, DimSupplier.supplier_id == DimParts.supplier_id
        ).join(
            DimPurchances, DimParts.part_id == DimPurchances.part_id
        ).group_by(
            DimSupplier.supplier_id,
            DimSupplier.supplier_name
        )

        if date_range:
            query = query.filter(
                DimPurchances.purchance_date.between(date_range.start_date, date_range.end_date)
            )

        return [
            {
                "supplier_id": row.supplier_id,
                "supplier_name": row.supplier_name,
                "total_transactions": row.total_transactions,
                "average_purchases": row.total_purchases,
                "average_warranties": row.total_warranties,
                "transaction_ratio": row.total_warranties / row.total_purchases if row.total_purchases > 0 else 0
            }
            for row in query.all()
        ]
    
    async def get_transactions_by_model(self, date_range: DateRangeFilter | None = None):
        """Analisa transações por modelo de veículo"""
        query = self.db.query(
            DimVehicle.model,
            DimVehicle.year,
            func.count(FactWarranties.claim_key).label('warranty_count'),
            func.count(distinct(DimParts.part_id)).label('unique_parts'),
            func.count(distinct(DimParts.supplier_id)).label('unique_suppliers')
        ).join(
            FactWarranties, DimVehicle.vehicle_id == FactWarranties.vehicle_id
        ).join(
            DimParts, FactWarranties.part_id == DimParts.part_id
        ).group_by(
            DimVehicle.model,
            DimVehicle.year
        )

        if date_range:
            query = query.filter(
                FactWarranties.repair_date.between(date_range.start_date, date_range.end_date)
            )

        return [
            {
                "model": row.model,
                "year": row.year,
                "warranty_count": row.warranty_count,
                "unique_parts": row.unique_parts,
                "unique_suppliers": row.unique_suppliers
            }
            for row in query.all()
        ]

    async def get_part_performance_analytics(self, date_range: DateRangeFilter | None = None):
        """Analisa o desempenho das peças baseado em garantias"""
        query = self.db.query(
            DimParts.part_id,
            DimParts.part_name,
            DimSupplier.supplier_name,
            func.count(FactWarranties.claim_key).label('warranty_count'),
            func.count(distinct(FactWarranties.classifed_as)).label('failure_types')
        ).join(
            DimSupplier, DimParts.supplier_id == DimSupplier.supplier_id
        ).join(
            FactWarranties, DimParts.part_id == FactWarranties.part_id
        ).group_by(
            DimParts.part_id,
            DimParts.part_name,
            DimSupplier.supplier_name
        )

        if date_range:
            query = query.filter(
                FactWarranties.repair_date.between(date_range.start_date, date_range.end_date)
            )

        return [
            {
                "part_id": row.part_id,
                "part_name": row.part_name,
                "supplier_name": row.supplier_name,
                "warranty_count": row.warranty_count,
                "failure_types": row.failure_types
            }
            for row in query.all()
        ]
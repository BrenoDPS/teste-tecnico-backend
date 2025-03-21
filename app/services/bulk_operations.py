from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.models import DimVehicle, DimParts, DimSupplier, DimLocations, DimPurchances, FactWarranties
from ..schemas.bulk_operations import (
    BulkCreateVehicle, BulkCreatePart, BulkCreateSupplier,
    DateRangeFilter, SupplierFilter, TransactionFilter
)

class BulkOperationsService:
    def __init__(self, db: Session):
        self.db = db

    async def bulk_create_vehicles(self, vehicles: BulkCreateVehicle) -> List[Dict[str, Any]]:
        db_vehicles = [DimVehicle(**vehicle.dict()) for vehicle in vehicles.vehicles]
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

    async def bulk_create_parts(self, parts: BulkCreatePart) -> List[Dict[str, Any]]:
        db_parts = [DimParts(**part.dict()) for part in parts.parts]
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

    async def get_supplier_sales_analytics(
        self,
        supplier_filter: SupplierFilter | None = None,
        date_range: DateRangeFilter | None = None
    ) -> List[Dict[str, Any]]:
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
    ) -> List[Dict[str, Any]]:
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

    async def get_transaction_analytics(
        self,
        transaction_filter: TransactionFilter | None = None
    ) -> Dict[str, Any]:
        purchases_query = self.db.query(
            func.count(DimPurchances.purchance_id).label('total_count'),
            DimPurchances.purchance_type
        ).group_by(DimPurchances.purchance_type)

        warranties_query = self.db.query(
            func.count(FactWarranties.claim_key).label('total_count')
        )

        if transaction_filter:
            if transaction_filter.date_range:
                purchases_query = purchases_query.filter(
                    DimPurchances.purchance_date.between(
                        transaction_filter.date_range.start_date,
                        transaction_filter.date_range.end_date
                    )
                )
                warranties_query = warranties_query.filter(
                    FactWarranties.repair_date.between(
                        transaction_filter.date_range.start_date,
                        transaction_filter.date_range.end_date
                    )
                )

        purchases_result = purchases_query.all()
        warranties_result = warranties_query.first()

        purchances_by_type = {
            row.purchance_type: {
                "total_count": row.total_count
            }
            for row in purchases_result
        }

        return {
            "purchases": purchances_by_type,
            "warranties": {
                "total_count": warranties_result.total_count if warranties_result else 0
            }
        } 
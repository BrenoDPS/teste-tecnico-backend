from datetime import date

from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..models.auth import User
from ..models.models import (
    DimLocations,
    DimParts,
    DimPurchances,
    DimSupplier,
    DimVehicle,
    FactWarranties,
)


def seed_locations(db: Session):
    locations = [
        {
            "market": "Mercado Interno",
            "country": "Brasil",
            "province": "Sao Paulo",
            "city": "Sorocaba",
        },
        {
            "market": "Mercado Internacional",
            "country": "Estados Unidos",
            "province": "California",
            "city": "Los Angeles",
        },
        {
            "market": "Mercado Internacional",
            "country": "Alemanha",
            "province": "Baviera",
            "city": "Munich",
        },
        {
            "market": "Mercado Interno",
            "country": "Brasil",
            "province": "Parana",
            "city": "Curitiba",
        },
    ]
    for location in locations:
        db_location = DimLocations(**location)
        db.add(db_location)
    db.commit()


def seed_vehicles(db: Session):
    vehicles = [
        {
            "model": "Sedan X",
            "prod_date": date(2022, 1, 1),
            "year": 2022,
            "propulsion": "COMBUSTION",
        },
        {
            "model": "SUV Y",
            "prod_date": date(2023, 1, 1),
            "year": 2023,
            "propulsion": "HYBRID",
        },
        {
            "model": "Hatch Z",
            "prod_date": date(2021, 6, 1),
            "year": 2021,
            "propulsion": "ELECTRIC",
        },
    ]
    for vehicle in vehicles:
        db_vehicle = DimVehicle(**vehicle)
        db.add(db_vehicle)
    db.commit()


def seed_suppliers(db: Session):
    suppliers = [
        {"supplier_name": "Auto Peças Silva", "location_id": 1},
        {"supplier_name": "Peças e Cia", "location_id": 2},
        {"supplier_name": "Distribuidora XYZ", "location_id": 3},
    ]
    for supplier in suppliers:
        db_supplier = DimSupplier(**supplier)
        db.add(db_supplier)
    db.commit()


def seed_parts(db: Session):
    parts = [
        {"part_name": "Freio ABS", "last_id_purchase": 1, "supplier_id": 1},
        {"part_name": "Kit Suspensão", "last_id_purchase": 2, "supplier_id": 2},
        {"part_name": "Motor Elétrico", "last_id_purchase": 3, "supplier_id": 3},
    ]
    for part in parts:
        db_part = DimParts(**part)
        db.add(db_part)
    db.commit()


def seed_purchances(db: Session):
    purchances = [
        {"purchance_type": "COMPRA", "purchance_date": date(2024, 3, 1), "part_id": 1},
        {
            "purchance_type": "GARANTIA",
            "purchance_date": date(2024, 3, 2),
            "part_id": 2,
        },
        {"purchance_type": "COMPRA", "purchance_date": date(2024, 3, 3), "part_id": 3},
    ]
    for purchance in purchances:
        db_purchance = DimPurchances(**purchance)
        db.add(db_purchance)
    db.commit()


def seed_warranties(db: Session):
    warranties = [
        {
            "vehicle_id": 1,
            "claim_key": 1001,
            "repair_date": date(2024, 3, 2),
            "client_comment": "Problema no freio",
            "tech_comment": "Substituição do módulo ABS",
            "part_id": 1,
            "classifed_as": "MECHANICAL",
            "location_id": 1,
            "purchance_id": 2,
        },
        {
            "vehicle_id": 2,
            "claim_key": 1002,
            "repair_date": date(2024, 3, 3),
            "client_comment": "Ruído na suspensão",
            "tech_comment": "Troca dos amortecedores",
            "part_id": 2,
            "classifed_as": "MECHANICAL",
            "location_id": 2,
            "purchance_id": 2,
        },
        {
            "vehicle_id": 3,
            "claim_key": 1003,
            "repair_date": date(2024, 3, 4),
            "client_comment": "Falha no motor",
            "tech_comment": "Substituição do motor elétrico",
            "part_id": 3,
            "classifed_as": "ELECTRICAL",
            "location_id": 3,
            "purchance_id": 2,
        },
    ]
    for warranty in warranties:
        db_warranty = FactWarranties(**warranty)
        db.add(db_warranty)
    db.commit()


def seed_users(db: Session):
    users = [
        {
            "email": "admin@mail.com",
            "username": "admin",
            "hashed_password": get_password_hash("admin123"),
            "is_active": True,
            "is_superuser": True,
        },
        {
            "email": "user@mail.com",
            "username": "user",
            "hashed_password": get_password_hash("user123"),
            "is_active": True,
            "is_superuser": False,
        },
    ]
    for user in users:
        db_user = User(**user)
        db.add(db_user)
    db.commit()


def seed_all(db: Session):
    """Função principal para popular todas as tabelas na ordem correta"""
    seed_locations(db)
    seed_vehicles(db)
    seed_suppliers(db)
    seed_parts(db)
    seed_purchances(db)
    seed_warranties(db)
    seed_users(db)

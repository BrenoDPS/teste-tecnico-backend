from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..db.database import Base
# criptografia para CPF
from cryptography.fernet import Fernet
from ..core.settings import settings
from ..core.security import encrypt_value, decrypt_value


class DimVehicle(Base):
    __tablename__ = "dim_vehicle"

    vehicle_id = Column(Integer, primary_key=True, index=True)
    model = Column(String(255))
    prod_date = Column(Date)
    year = Column(Integer)
    propulsion = Column(String)  # ENUM no banco de dados

    warranties = relationship("FactWarranties", back_populates="vehicle")

class DimParts(Base):
    __tablename__ = "dim_parts"

    part_id = Column(Integer, primary_key=True, index=True)
    part_name = Column(String(255))
    last_id_purchase = Column(Integer)
    supplier_id = Column(Integer, ForeignKey("dim_supplier.supplier_id"))

    supplier = relationship("DimSupplier", back_populates="parts")
    warranties = relationship("FactWarranties", back_populates="part")

class DimSupplier(Base):
    __tablename__ = "dim_supplier"

    supplier_id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String(50))
    location_id = Column(Integer, ForeignKey("dim_locations.location_id"))
    _encrypted_cpf = Column("encrypted_cpf", String(255))

    location = relationship("DimLocations", back_populates="suppliers")
    parts = relationship("DimParts", back_populates="supplier")

    @property
    def cpf(self):
        """Getter para o CPF descriptografado"""
        if self._encrypted_cpf:
            return decrypt_value(self._encrypted_cpf)
        return None

    @cpf.setter
    def cpf(self, value: str):
        """Setter para criptografar o CPF antes de salvar"""
        if value:
            self._encrypted_cpf = encrypt_value(value)
        else:
            self._encrypted_cpf = None

            
class DimLocations(Base):
    __tablename__ = "dim_locations"

    location_id = Column(Integer, primary_key=True, index=True)
    market = Column(String(50))
    country = Column(String(50))
    province = Column(String(50))
    city = Column(String(50))

    suppliers = relationship("DimSupplier", back_populates="location")
    warranties = relationship("FactWarranties", back_populates="location")

class DimPurchances(Base):
    __tablename__ = "dim_purchances"

    purchance_id = Column(Integer, primary_key=True, index=True)
    purchance_type = Column(String)  # ENUM no banco de dados
    purchance_date = Column(Date)
    part_id = Column(Integer, ForeignKey("dim_parts.part_id"))

    warranties = relationship("FactWarranties", back_populates="purchance")

class FactWarranties(Base):
    __tablename__ = "fact_warranties"

    vehicle_id = Column(Integer, ForeignKey("dim_vehicle.vehicle_id"))
    claim_key = Column(Integer, primary_key=True)
    repair_date = Column(Date)
    client_comment = Column(Text)
    tech_comment = Column(Text)
    part_id = Column(Integer, ForeignKey("dim_parts.part_id"))
    classifed_as = Column(String(50))
    location_id = Column(Integer, ForeignKey("dim_locations.location_id"))
    purchance_id = Column(Integer, ForeignKey("dim_purchances.purchance_id"))

    vehicle = relationship("DimVehicle", back_populates="warranties")
    part = relationship("DimParts", back_populates="warranties")
    location = relationship("DimLocations", back_populates="warranties")
    purchance = relationship("DimPurchances", back_populates="warranties") 
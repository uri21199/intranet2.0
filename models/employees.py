from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config import Base

class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {"schema": "hr"}

    id = Column(Integer, primary_key=True, index=True)
    tax_id = Column(String(100), nullable=False, unique=True)  # CUIT
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=False)
    record_number = Column(Integer, nullable=False)  # Legajo
    gender = Column(String(5), nullable=True)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    state = Column(String(100), nullable=True)  # Provincia
    city = Column(String(100), nullable=True)   # Localidad
    address = Column(String(100), nullable=True)
    union_agreement = Column(Boolean, default=True, nullable=False)  # Convenio
    health_insurance = Column(Boolean, default=True, nullable=False)  # Prepaga
    department_id = Column(Integer, ForeignKey("general.departments.id", ondelete="SET NULL"))
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relación con departamentos
    department = relationship("Department", back_populates="employees")  # 📌 Esto corrige el error
    roles = relationship("Role", secondary="hr.employee_roles", back_populates="employees")

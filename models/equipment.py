from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class Equipment(Base):
    __tablename__ = "equipment"
    __table_args__ = {"schema": "hr"}

    id = Column(Integer, primary_key=True, index=True)
    equipment_type = Column(String(100), nullable=False)
    equipment_id = Column(String(100), unique=True, nullable=False)
    status = Column(String(50), default="Available")
    location = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=True)
    anydesk = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    file_path = Column(Text, nullable=True)
    area_id = Column(Integer, ForeignKey("general.departments.id", ondelete="SET NULL"), nullable=True)
    client_id = Column(Integer, ForeignKey("general.clients.id", ondelete="SET NULL"), nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relaciones
    user = relationship("Employee")
    area = relationship("Department")
    client = relationship("Client")

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": "documents"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(Text, nullable=False)
    document_type = Column(String(50), nullable=False)
    created_by = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=False)
    last_modified = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relación con empleados (creador del documento)
    created_by_employee = relationship("Employee")

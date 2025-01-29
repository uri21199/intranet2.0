from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class DocumentVersion(Base):
    __tablename__ = "document_versions"
    __table_args__ = {"schema": "documents"}

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.documents.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    file_path = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relaciones
    document = relationship("Document")
    created_by_employee = relationship("Employee")

from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class DocumentRole(Base):
    __tablename__ = "document_roles"
    __table_args__ = {"schema": "documents"}

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.documents.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("general.roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


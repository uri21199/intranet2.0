from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config import Base
from models.role_permissions import role_permissions  # Importamos la tabla intermedia

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "general"}

    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String(150), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relación con roles (muchos a muchos)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

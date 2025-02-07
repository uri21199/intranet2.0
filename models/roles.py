from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config import Base
from models.role_permissions import role_permissions  # Importamos la tabla intermedia

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "general"}  # Indicar el esquema

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relación con permisos (muchos a muchos)
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

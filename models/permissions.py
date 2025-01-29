from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "general"}

    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String(150), nullable=False)
    role_id = Column(Integer, ForeignKey("general.roles.id", ondelete="CASCADE"), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relación con Roles
    role = relationship("Role", back_populates="permissions")

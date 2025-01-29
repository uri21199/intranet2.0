from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from config import Base  # Importamos `Base` desde config.py

class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {"schema": "general"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

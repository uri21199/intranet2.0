from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from config import Base

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = {"schema": "general"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    country = Column(String(100), nullable=False)
    main_contact = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)
    active = Column(Boolean, default=True)
    services = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

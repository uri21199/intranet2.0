from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config import Base

class TicketCategory(Base):
    __tablename__ = "ticket_categories"
    __table_args__ = {"schema": "tickets"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relación con TicketSubcategory
    subcategories = relationship("TicketSubcategory", back_populates="category", cascade="all, delete-orphan")

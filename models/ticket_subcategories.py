from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class TicketSubcategory(Base):
    __tablename__ = "ticket_subcategories"
    __table_args__ = {"schema": "tickets"}

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("tickets.ticket_categories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relación con TicketCategory
    category = relationship("TicketCategory", back_populates="subcategories")

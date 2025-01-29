from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class TicketUpdate(Base):
    __tablename__ = "ticket_updates"
    __table_args__ = {"schema": "tickets"}

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.system_tickets.id", ondelete="CASCADE"), nullable=False)
    updated_by = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=False)
    description = Column(Text, nullable=False)
    previous_status = Column(String(50), nullable=True)
    current_status = Column(String(50), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now())


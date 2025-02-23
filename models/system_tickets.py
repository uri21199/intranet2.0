from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class SystemTicket(Base):
    __tablename__ = "system_tickets"
    __table_args__ = {"schema": "tickets"}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("tickets.ticket_categories.id", ondelete="CASCADE"), nullable=False)
    subcategory_id = Column(Integer, ForeignKey("tickets.ticket_subcategories.id", ondelete="SET NULL"), nullable=True)
    description = Column(Text, nullable=False)
    status_id = Column(Integer, ForeignKey("tickets.ticket_statuses.id", ondelete="SET NULL"), nullable=True)
    assigned_to = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    closed_at = Column(TIMESTAMP, nullable=True)

    # Relaciones
    employee = relationship("Employee", foreign_keys=[employee_id])
    category = relationship("TicketCategory")
    subcategory = relationship("TicketSubcategory")
    assigned_employee = relationship("Employee", foreign_keys=[assigned_to])
    status = relationship("TicketStatus")

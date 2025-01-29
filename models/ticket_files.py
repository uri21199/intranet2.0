from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class TicketFile(Base):
    __tablename__ = "ticket_files"
    __table_args__ = {"schema": "tickets"}

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.system_tickets.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(150), nullable=False)
    file_path = Column(Text, nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())

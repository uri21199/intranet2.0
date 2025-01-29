from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class ABMRequest(Base):
    __tablename__ = "abm_requests"
    __table_args__ = {"schema": "tickets"}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    request_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="Pending")
    request_date = Column(TIMESTAMP, server_default=func.now())
    processed_by = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=True)

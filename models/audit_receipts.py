from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class AuditReceipt(Base):
    __tablename__ = "audit_receipts"
    __table_args__ = {"schema": "logs"}

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("hr.salary_receipts.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(50), nullable=False)
    date = Column(TIMESTAMP, server_default=func.now())
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=False)

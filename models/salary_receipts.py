from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from config import Base

class SalaryReceipt(Base):
    __tablename__ = "salary_receipts"
    __table_args__ = {"schema": "hr"}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    signed = Column(Boolean, default=False)
    file_path = Column(Text, nullable=True)
    signature_date = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

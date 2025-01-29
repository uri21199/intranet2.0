from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class ChangeHistory(Base):
    __tablename__ = "change_history"
    __table_args__ = {"schema": "logs"}

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(150), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    changed_by = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=False)
    change_date = Column(TIMESTAMP, server_default=func.now())
    details = Column(Text, nullable=True)

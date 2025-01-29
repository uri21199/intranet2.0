from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Date, ForeignKey
from sqlalchemy.sql import func
from config import Base

class Training(Base):
    __tablename__ = "trainings"
    __table_args__ = {"schema": "trainings"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    training_date = Column(Date, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    responsible_employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

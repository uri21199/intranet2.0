from sqlalchemy import Column, Integer, Text, TIMESTAMP, Date, ForeignKey
from sqlalchemy.sql import func
from config import Base

class TrainedEmployee(Base):
    __tablename__ = "trained_employees"
    __table_args__ = {"schema": "trainings"}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    training_id = Column(Integer, ForeignKey("trainings.trainings.id", ondelete="CASCADE"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    observations = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

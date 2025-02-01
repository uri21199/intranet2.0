from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class TravelAssistance(Base):
    __tablename__ = "travel_assistance"
    __table_args__ = {"schema": "hr"}  # Define el esquema

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    vacation_request_id = Column(Integer, ForeignKey("hr.requested_days.id", ondelete="CASCADE"), nullable=False)
    travel_assistance = Column(Integer, default=False, nullable=False)  # 0 = No, 1 = Sí
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    employee = relationship("Employee", back_populates="travel_assistance")
    vacation_request = relationship("RequestedDay", back_populates="travel_assistance")

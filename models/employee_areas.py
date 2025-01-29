from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class EmployeeArea(Base):
    __tablename__ = "employee_areas"
    __table_args__ = {"schema": "general"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    area_id = Column(Integer, ForeignKey("general.departments.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

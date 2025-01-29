from sqlalchemy import Column, Integer, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class DepartmentHead(Base):
    __tablename__ = "department_heads"
    __table_args__ = {"schema": "general"}

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("general.departments.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

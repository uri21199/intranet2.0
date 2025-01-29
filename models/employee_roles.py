from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class EmployeeRole(Base):
    __tablename__ = "employee_roles"
    __table_args__ = {"schema": "hr"}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("general.roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


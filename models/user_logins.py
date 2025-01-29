from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class UserLogin(Base):
    __tablename__ = "user_logins"
    __table_args__ = {"schema": "logs"}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    login_time = Column(TIMESTAMP, server_default=func.now())
    success = Column(Boolean, nullable=False)

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {"schema": "logs"}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=True)
    role_id = Column(Integer, ForeignKey("general.roles.id", ondelete="CASCADE"), nullable=True)
    department_id = Column(Integer, ForeignKey("general.departments.id", ondelete="CASCADE"), nullable=True)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    status = Column(String(20), default="Unread")
    created_at = Column(TIMESTAMP, server_default=func.now())

from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class AreaMail(Base):
    __tablename__ = "areas_mails"
    __table_args__ = {"schema": "general"}

    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("general.departments.id", ondelete="CASCADE"), nullable=False)
    mail_id = Column(Integer, ForeignKey("general.mails.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

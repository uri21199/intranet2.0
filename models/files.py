from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class File(Base):
    __tablename__ = "files"
    __table_args__ = {"schema": "documents"}

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(150), nullable=False)
    file_path = Column(Text, nullable=False)
    request_id = Column(Integer, ForeignKey("hr.requested_days.id", ondelete="CASCADE"), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from config import Base

class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = {"schema": "rooms"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String(255), nullable=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

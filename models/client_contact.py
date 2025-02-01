from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class ClientContact(Base):
    __tablename__ = "client_contacts"
    __table_args__ = {"schema": "general"}  # Define el esquema

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("general.clients.id", ondelete="CASCADE"), nullable=False)
    contact_name = Column(String(150), nullable=False)
    position = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(150), nullable=False, unique=True)
    contact_hours = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    client = relationship("Client", back_populates="contacts")

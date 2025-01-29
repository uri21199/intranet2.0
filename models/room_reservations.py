from sqlalchemy import Column, Integer, String, Text, Date, Time, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config import Base

class RoomReservation(Base):
    __tablename__ = "room_reservations"
    __table_args__ = {"schema": "rooms"}

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.rooms.id", ondelete="CASCADE"), nullable=False)
    reserved_by = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=False)
    client_id = Column(Integer, ForeignKey("general.clients.id", ondelete="SET NULL"), nullable=True)
    use = Column(String(100), default="Capacitación")
    justification = Column(Text, nullable=True)
    status = Column(String(50), default="Pending")
    authorized_by = Column(Integer, ForeignKey("hr.employees.id", ondelete="SET NULL"), nullable=True)
    reservation_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relaciones
    room = relationship("Room")
    reserved_employee = relationship("Employee", foreign_keys=[reserved_by])
    client = relationship("Client")
    authorized_employee = relationship("Employee", foreign_keys=[authorized_by])

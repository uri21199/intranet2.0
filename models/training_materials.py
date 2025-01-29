from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class TrainingMaterial(Base):
    __tablename__ = "training_materials"
    __table_args__ = {"schema": "trainings"}

    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.trainings.id", ondelete="CASCADE"), nullable=False)
    material_name = Column(String(150), nullable=False)
    material_type = Column(String(50), nullable=False)
    material_url = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class SurveyArea(Base):
    __tablename__ = "survey_areas"
    __table_args__ = {"schema": "surveys"}

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.surveys.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(Integer, ForeignKey("general.departments.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

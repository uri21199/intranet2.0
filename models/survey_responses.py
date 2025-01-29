from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class SurveyResponse(Base):
    __tablename__ = "survey_responses"
    __table_args__ = {"schema": "surveys"}

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.surveys.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    response_text = Column(Text, nullable=False)
    response_date = Column(TIMESTAMP, server_default=func.now())

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class SurveyQuestion(Base):
    __tablename__ = "survey_questions"
    __table_args__ = {"schema": "surveys"}

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.surveys.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

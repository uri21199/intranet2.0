from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class SurveyAnswer(Base):
    __tablename__ = "survey_answers"
    __table_args__ = {"schema": "surveys"}

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("surveys.survey_questions.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("hr.employees.id", ondelete="CASCADE"), nullable=False)
    answer_text = Column(Text, nullable=True)
    answer_option = Column(Integer, nullable=True)
    response_date = Column(TIMESTAMP, server_default=func.now())

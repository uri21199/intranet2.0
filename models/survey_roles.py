from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class SurveyRole(Base):
    __tablename__ = "survey_roles"
    __table_args__ = {"schema": "surveys"}

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.surveys.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("general.roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

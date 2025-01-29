from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config import Base

class NewsRole(Base):
    __tablename__ = "news_roles"
    __table_args__ = {"schema": "general"}

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey("general.internal_news.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("general.roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

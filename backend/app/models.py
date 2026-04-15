from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class Objection(Base):
    __tablename__ = "objections"

    id = Column(Integer, primary_key=True, index=True)
    objection_text = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    embedding = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

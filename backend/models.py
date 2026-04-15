from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class AgentStatus(str, enum.Enum):
    active = "active"
    idle = "idle"
    error = "error"

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Enum(AgentStatus), default=AgentStatus.idle)
    created_at = Column(DateTime, default=datetime.utcnow)
    logs = relationship("Log", back_populates="agent")

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    message = Column(Text, nullable=False)
    level = Column(String(20), default="info")
    timestamp = Column(DateTime, default=datetime.utcnow)
    agent = relationship("Agent", back_populates="logs")

class Objection(Base):
    __tablename__ = "objections"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

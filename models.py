from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Mood(Base):
    __tablename__ = "moods"
    id = Column(Integer, primary_key=True, index=True)
    mood = Column(String)
    score = Column(Integer, default=3)
    timestamp = Column(DateTime, default=datetime.utcnow)

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    mood = Column(String)
    tags = Column(String, default="")
    timestamp = Column(DateTime, default=datetime.utcnow)
class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    goal_type = Column(String)   # "wellbeing", "life", "micro"
    status = Column(String, default="active")  # "active", "completed", "abandoned"
    created_at = Column(DateTime, default=datetime.utcnow)
    last_checkin = Column(DateTime, nullable=True)    
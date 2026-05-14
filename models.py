from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="default")
    role = Column(String)
    content = Column(Text)
    crisis_flag = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Mood(Base):
    __tablename__ = "moods"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="default")
    mood = Column(String)
    note = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="default")
    content = Column(Text)
    mood = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="default")
    title = Column(String)
    description = Column(Text)
    goal_type = Column(String)   # "wellbeing", "life", "micro"
    status = Column(String, default="active")  # "active", "completed", "abandoned"
    progress_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_checkin = Column(DateTime, nullable=True)
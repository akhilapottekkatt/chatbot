from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


GoalType = Literal["wellbeing", "life", "micro"]
GoalStatus = Literal["active", "completed", "abandoned"]


class ChatInput(BaseModel):
    user_id: str = Field(default="default", min_length=1)
    message: str = Field(min_length=1)


class ChatOutput(BaseModel):
    response: str
    crisis: bool = False


class MoodCreate(BaseModel):
    user_id: str = Field(default="default", min_length=1)
    mood: str = Field(min_length=1)
    note: Optional[str] = None


class JournalCreate(BaseModel):
    user_id: str = Field(default="default", min_length=1)
    content: str = Field(min_length=1)
    mood: Optional[str] = None


class GoalCreate(BaseModel):
    user_id: str = Field(default="default", min_length=1)
    title: str = Field(min_length=1)
    description: Optional[str] = None
    goal_type: GoalType = "wellbeing"


class GoalCheckinUpdate(BaseModel):
    status: GoalStatus = "active"
    progress_note: Optional[str] = None
    last_checkin: datetime = Field(default_factory=datetime.utcnow)

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import MoodCreate
from services.suggestions import suggestion_for_mood

router = APIRouter(prefix="/api/mood", tags=["mood"])

@router.post("")
def create_mood(payload: MoodCreate, db: Session = Depends(get_db)):
    mood = models.Mood(
        user_id=payload.user_id,
        mood=payload.mood,
        score=payload.score,
        note=payload.note,
    )
    db.add(mood)
    db.commit()
    db.refresh(mood)
    return {"id": mood.id, "mood": mood.mood, "score": mood.score, "timestamp": mood.timestamp}

@router.get("/latest/{user_id}")
def latest_mood(user_id: str, db: Session = Depends(get_db)):
    latest = (
        db.query(models.Mood)
        .filter(models.Mood.user_id == user_id)
        .order_by(desc(models.Mood.timestamp))
        .first()
    )
    if not latest:
        return {"mood": None, "score": None, "suggestions": suggestion_for_mood(None)}
    return {"mood": latest.mood, "score": latest.score, "suggestions": suggestion_for_mood(latest.mood)}
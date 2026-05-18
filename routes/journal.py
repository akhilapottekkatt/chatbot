from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import JournalCreate

router = APIRouter(prefix="/api/journal", tags=["journal"])

@router.post("")
def create_entry(payload: JournalCreate, db: Session = Depends(get_db)):
    entry = models.JournalEntry(
        user_id=payload.user_id,
        content=payload.content,
        mood=payload.mood or "",
        tags=payload.tags or "",  # ✅ your addition
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"id": entry.id, "timestamp": entry.timestamp}

@router.get("/{user_id}")
def list_entries(user_id: str, limit: int = 10, db: Session = Depends(get_db)):
    entries = (
        db.query(models.JournalEntry)
        .filter(models.JournalEntry.user_id == user_id)
        .order_by(desc(models.JournalEntry.timestamp))
        .limit(limit)
        .all()
    )
    return [
        {
            "id": row.id,
            "content": row.content,
            "mood": row.mood,
            "tags": row.tags,  # ✅ your addition
            "timestamp": row.timestamp
        }
        for row in entries
    ]
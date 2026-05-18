from sqlalchemy import desc
from sqlalchemy.orm import Session
import models

def build_user_context(db: Session, user_id: str) -> str:
    latest_mood = (
        db.query(models.Mood)
        .filter(models.Mood.user_id == user_id)
        .order_by(desc(models.Mood.timestamp))
        .first()
    )
    active_goals = (
        db.query(models.Goal)
        .filter(models.Goal.user_id == user_id, models.Goal.status == "active")
        .order_by(desc(models.Goal.created_at))
        .limit(3)
        .all()
    )
    recent_journal = (
        db.query(models.JournalEntry)
        .filter(models.JournalEntry.user_id == user_id)
        .order_by(desc(models.JournalEntry.timestamp))
        .limit(3)
        .all()
    )

    # your addition ✅ - includes score
    mood_text = (
        f"{latest_mood.mood} (score {latest_mood.score}/5)"
        if latest_mood else "unknown"
    )
    goals_text = ", ".join(goal.title for goal in active_goals) or "none"
    journal_text = " | ".join(entry.content[:120] for entry in recent_journal) or "none"

    return (
        f"User mood: {mood_text}\n"
        f"Active goals: {goals_text}\n"
        f"Recent journal snippets: {journal_text}"
    )
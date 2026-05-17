from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import GoalCheckinUpdate, GoalCreate

router = APIRouter(prefix="/api/goals", tags=["goals"])

@router.post("")
def create_goal(payload: GoalCreate, db: Session = Depends(get_db)):
    goal = models.Goal(
        user_id=payload.user_id,
        title=payload.title,
        description=payload.description or "",
        goal_type=payload.goal_type,
        status="active",
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return {"id": goal.id, "title": goal.title, "goal_type": goal.goal_type}

@router.get("/{user_id}")
def list_goals(user_id: str, db: Session = Depends(get_db)):
    goals = (
        db.query(models.Goal)
        .filter(models.Goal.user_id == user_id)
        .order_by(desc(models.Goal.created_at))
        .all()
    )
    return [
        {
            "id": row.id,
            "title": row.title,
            "description": row.description,
            "goal_type": row.goal_type,
            "status": row.status,
            "last_checkin": row.last_checkin,
            "progress_note": row.progress_note,
        }
        for row in goals
    ]

@router.patch("/{goal_id}/checkin")
def weekly_checkin(goal_id: int, payload: GoalCheckinUpdate, db: Session = Depends(get_db)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    goal.status = payload.status
    goal.progress_note = payload.progress_note
    goal.last_checkin = payload.last_checkin
    db.commit()
    db.refresh(goal)
    return {"id": goal.id, "status": goal.status, "last_checkin": goal.last_checkin}
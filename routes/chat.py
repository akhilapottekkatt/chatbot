from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import ChatInput, ChatOutput
from services.ai_client import generate_chat_reply
from services.context import build_user_context
from services.crisis import SAFE_RESPONSE, keyword_crisis_detected, ai_crisis_detected

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatOutput)
def chat(data: ChatInput, db: Session = Depends(get_db)):
    db.add(models.Message(user_id=data.user_id, role="user", content=data.message))
    db.commit()

    if keyword_crisis_detected(data.message):
        db.add(models.Message(
            user_id=data.user_id,
            role="bot",
            content=SAFE_RESPONSE,
            crisis_flag=True,
        ))
        db.commit()
        return ChatOutput(response=SAFE_RESPONSE, crisis=True)

    if ai_crisis_detected(data.message):
        db.add(models.Message(
            user_id=data.user_id,
            role="bot",
            content=SAFE_RESPONSE,
            crisis_flag=True,
        ))
        db.commit()
        return ChatOutput(response=SAFE_RESPONSE, crisis=True)

    context = build_user_context(db, data.user_id)
    reply = generate_chat_reply(data.message, context, data.include_context)

    db.add(models.Message(user_id=data.user_id, role="bot", content=reply))
    db.commit()

    return ChatOutput(response=reply, crisis=False)
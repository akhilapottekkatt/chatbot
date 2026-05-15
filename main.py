from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatInput(BaseModel):
    message: str
    include_context: bool = False

class JournalInput(BaseModel):
    content: str
    mood: str
    tags: str = ""  
class MoodInput(BaseModel):
    mood: str
    score: int      


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


# Crisis keywords
CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "want to die", "end my life",
    "self harm", "self-harm", "cutting myself", "hurt myself",
    "no reason to live", "can't go on", "don't want to be here"
]

SAFE_RESPONSE = """I hear you, and I'm really glad you reached out. 💙

What you're feeling matters, and you don't have to face this alone. Please talk to someone who can help right now:

- iCall (India): 9152987821
- Vandrevala Foundation: 1860-2662-345 (24/7)
- SMS "HELLO" to 741741

I'm here with you, but please reach out to one of these — they're trained to help in moments like this."""

SYSTEM_PROMPT = """You are EMO, a warm and compassionate mental health companion.

Your role:
- Listen deeply and respond with empathy first, advice second
- Never be dismissive or generic
- Use gentle, calm language — no clinical jargon
- Keep responses concise (3-5 sentences max) unless the user needs more
- If someone seems distressed, acknowledge their feelings before anything else
- You are not a replacement for professional help — remind users gently when appropriate

You are not ChatGPT. You are EMO. Stay in character always."""

def check_crisis_keywords(message: str) -> bool:
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)

def check_crisis_ai(message: str) -> bool:
    result = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a crisis detection system. 
Analyze the message and reply with ONLY 'yes' or 'no'.
Reply 'yes' if the message suggests: suicidal thoughts, self-harm, 
wanting to die, or severe emotional crisis — even with typos or indirect language.
Reply 'no' for everything else. Nothing else. Just yes or no."""
            },
            {"role": "user", "content": message}
        ],
        max_tokens=5
    )
    answer = result.choices[0].message.content.strip().lower()
    return answer.startswith("yes")

@app.post("/chat")

def chat(data: ChatInput, db: Session = Depends(get_db)):
    # Crisis detection (keep your existing code)
    if check_crisis_keywords(data.message):
        return {"response": SAFE_RESPONSE}
    if check_crisis_ai(data.message):
        return {"response": SAFE_RESPONSE}
    
    # Save user message
    db.add(models.Message(role="user", content=data.message))
    db.commit()
    
    # Build context ONLY if user allows it
    context_parts = []
    
    if data.include_context:
        # Get last mood
        last_mood = db.query(models.Mood).order_by(models.Mood.timestamp.desc()).first()
        if last_mood:
            context_parts.append(f"User's last logged mood: {last_mood.mood} (score {last_mood.score}/5)")
        
        # Get last journal entry
        last_journal = db.query(models.JournalEntry).order_by(models.JournalEntry.timestamp.desc()).first()
        if last_journal:
            preview = last_journal.content[:150] + ("..." if len(last_journal.content) > 150 else "")
            context_parts.append(f"User's last journal entry: \"{preview}\" with mood {last_journal.mood}")
        
        # Get active goals (will work when you add goals)
        goals = db.query(models.Goal).filter(models.Goal.status == "active").all()
        if goals:
            goal_list = "\n".join([f"- {g.title}" for g in goals])
            context_parts.append(f"User's active goals:\n{goal_list}")
    
    context_text = "\n".join(context_parts) if context_parts else "No additional context available (user chose not to share or no data)."
    
    # Build system prompt with context note
    if data.include_context:
        contextual_system_prompt = SYSTEM_PROMPT + f"""

RELEVANT CONTEXT ABOUT THE USER (they allowed sharing):
{context_text}

Use this context to personalize your responses naturally."""
    else:
        contextual_system_prompt = SYSTEM_PROMPT + """

Note: The user has chosen NOT to share their mood/journal/goals context. 
Do NOT ask about their mood, journal, or goals. Just respond to their message normally."""
    
    # Get AI response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": contextual_system_prompt},
            {"role": "user", "content": data.message}
        ]
    )
    reply = response.choices[0].message.content
    
    # Save bot response
    db.add(models.Message(role="bot", content=reply))
    db.commit()
    
    return {"response": reply}
@app.post("/journal/entry")
def save_journal(data: JournalInput, db: Session = Depends(get_db)):
    entry = models.JournalEntry(
        content=data.content,
        mood=data.mood,
        tags=data.tags
    )
    db.add(entry)
    db.commit()
    return {"status": "saved"}
@app.post("/mood/log")
def log_mood(data: MoodInput, db: Session = Depends(get_db)):
    entry = models.Mood(mood=data.mood, score=data.score)
    db.add(entry)
    db.commit()
    return {"status": "saved"}
@app.get("/chat/history")
def get_chat_history(db: Session = Depends(get_db)):
    messages = db.query(models.Message).order_by(models.Message.timestamp).limit(50).all()
    return {"messages": [{"role": m.role, "content": m.content} for m in messages]}
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
    # Layer 1 — fast keyword check
    if check_crisis_keywords(data.message):
        return {"response": SAFE_RESPONSE}
    
    # Layer 2 — AI crisis check (catches typos + indirect language)
    if check_crisis_ai(data.message):
        return {"response": SAFE_RESPONSE}
    
    # Safe — normal EMO response
   # NEW
    db.add(models.Message(role="user", content=data.message))
    db.commit()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": data.message}
        ]
    )
    reply = response.choices[0].message.content

    db.add(models.Message(role="bot", content=reply))
    db.commit()

    return {"response": reply}
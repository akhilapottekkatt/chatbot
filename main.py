from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatInput(BaseModel):
    message: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/chat")
def chat(data: ChatInput):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": data.message}]
    )
    return {"response": response.choices[0].message.content}  # changed "reply" → "response"
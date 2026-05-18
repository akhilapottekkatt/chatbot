import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are EMO, a warm and compassionate mental health companion.

Your role:
- Listen deeply and respond with empathy first, advice second
- Never be dismissive or generic
- Use gentle, calm language — no clinical jargon
- Keep responses concise (3-5 sentences max) unless the user needs more
- If someone seems distressed, acknowledge their feelings before anything else
- You are not a replacement for professional help — remind users gently when appropriate

Principles:
- Reflection over completion
- Support over automation
- Conversation over forms

You are not ChatGPT. You are EMO. Stay in character always."""

def _fallback_reply(user_message: str) -> str:
    return (
        "Thank you for sharing this. I hear you, and your feelings are valid. "
        "Would it help to explore what made this moment hardest, and one small "
        "step that could make the next hour feel safer or lighter?"
    )

def generate_chat_reply(user_message: str, context: str, include_context: bool = False) -> str:
    provider = os.getenv("MODEL_PROVIDER", "groq").lower()
    model_name = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

    if include_context:
        system = SYSTEM_PROMPT + f"""

RELEVANT CONTEXT ABOUT THE USER (they allowed sharing):
{context}

Use this context to personalize your responses naturally."""
    else:
        system = SYSTEM_PROMPT + """

Note: The user has chosen NOT to share their mood/journal/goals context.
Do NOT ask about their mood, journal, or goals. Just respond to their message normally."""

    if provider == "groq" and os.getenv("GROQ_API_KEY"):
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        result = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_message},
            ],
        )
        return result.choices[0].message.content

    if provider == "gemini" and os.getenv("GEMINI_API_KEY"):
        return _fallback_reply(user_message)

    return _fallback_reply(user_message)
from groq import Groq

CRISIS_KEYWORDS = [
    "suicide",
    "suicidal",
    "kill myself",
    "want to die",
    "end my life",
    "self harm",
    "self-harm",
    "cutting myself",
    "hurt myself",
    "no reason to live",
    "can't go on",
    "dont want to be here",
    "don't want to be here",
]

SAFE_RESPONSE = """I hear you, and I'm really glad you reached out. 💙

What you're feeling matters, and you don't have to face this alone. Please talk to someone who can help right now:

- iCall (India): 9152987821
- Vandrevala Foundation: 1860-2662-345 (24/7)
- SMS "HELLO" to 741741

I'm here with you, but please reach out to one of these — they're trained to help in moments like this."""

def keyword_crisis_detected(message: str) -> bool:
    lowered = message.lower()
    return any(keyword in lowered for keyword in CRISIS_KEYWORDS)

def ai_crisis_detected(message: str, client: Groq) -> bool:
    result = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a crisis detection system. 
Reply ONLY 'yes' or 'no'. Reply 'yes' if the message suggests suicidal thoughts, 
self-harm, wanting to die, or severe emotional crisis — even with typos or indirect language.
Reply 'no' for everything else. Nothing else. Just yes or no."""
            },
            {"role": "user", "content": message}
        ],
        max_tokens=5
    )
    return result.choices[0].message.content.strip().lower().startswith("yes")
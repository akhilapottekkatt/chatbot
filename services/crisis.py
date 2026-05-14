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

SAFE_RESPONSE = """I hear you, and I am really glad you reached out.

What you are feeling matters, and you do not have to face it alone.
Please contact immediate support in your region right now:
- If there is immediate danger, call local emergency services.
- If available, contact a local crisis helpline.

I can stay with you here while you take that step."""


def keyword_crisis_detected(message: str) -> bool:
    lowered = message.lower()
    return any(keyword in lowered for keyword in CRISIS_KEYWORDS)

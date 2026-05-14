from typing import List, Optional

SUGGESTIONS_BY_MOOD = {
    "anxious": [
        "Try box breathing for 2 minutes.",
        "Ground yourself with 5-4-3-2-1 sensory check.",
    ],
    "sad": [
        "Take a short walk and get fresh air.",
        "Write one kind sentence to yourself.",
    ],
    "stressed": [
        "Take a 5-minute break away from screens.",
        "Do a gentle shoulder and neck stretch.",
    ],
    "happy": [
        "Capture what helped you feel good today.",
        "Share this moment with someone you trust.",
    ],
}

DEFAULT_SUGGESTIONS = [
    "Take three slow breaths.",
    "Drink water and check in with your body.",
]


def suggestion_for_mood(mood: Optional[str]) -> List[str]:
    if not mood:
        return DEFAULT_SUGGESTIONS
    return SUGGESTIONS_BY_MOOD.get(mood.lower(), DEFAULT_SUGGESTIONS)

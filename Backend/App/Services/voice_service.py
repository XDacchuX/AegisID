import random
import string
from typing import Dict

class VoiceService:
    _challenges: Dict[str, str] = {}

    @classmethod
    def generate_challenge(cls, user_id: str) -> str:
        words = ["blue", "tiger", "red", "moon", "fast", "wind", "dark", "star"]
        phrase = f"Say: {random.choice(words)} {random.choice(words)} {random.randint(100, 999)}"
        cls._challenges[user_id] = phrase
        return phrase

    @classmethod
    def verify_transcript(cls, user_id: str, transcript: str) -> dict:
        expected = cls._challenges.pop(user_id, "").replace("Say: ", "").lower()
        if not expected:
            return {"liveness": False, "reason": "Challenge expired"}

        words_expected = set(expected.split())
        words_received = set(transcript.lower().split())
        match_score = len(words_expected & words_received) / len(words_expected)

        return {
            "liveness": match_score >= 0.75,
            "score": round(match_score, 2),
            "expected": expected
        }

from antigravity_jarvis.config.settings import Settings


class ModeRouter:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def select_mode(self, text: str) -> str:
        lowered = text.lower()
        if any(word in lowered for word in ("code", "debug", "script", "engineer", "hacker")):
            return "engineer"
        if any(word in lowered for word in ("study", "teach", "notes", "exam")):
            return "student"
        if any(word in lowered for word in ("business", "revenue", "strategy", "ceo")):
            return "ceo"
        if any(word in lowered for word in ("motivate", "encourage", "confidence")):
            return "motivational"
        return self.settings.assistant.default_mode

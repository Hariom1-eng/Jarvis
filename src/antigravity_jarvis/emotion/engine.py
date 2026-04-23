from antigravity_jarvis.api.schemas import EmotionState
from antigravity_jarvis.config.settings import Settings


class EmotionEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def detect(self, text: str) -> EmotionState:
        lowered = text.lower()
        if any(word in lowered for word in ("stress", "worried", "upset", "sad")):
            return EmotionState("concerned", 0.88, "concern", "#7FD1FF")
        if any(word in lowered for word in ("great", "done", "won", "success")):
            return EmotionState("celebratory", 0.84, "excited", "#3DFFF3")
        if "diagnostics" in lowered:
            return EmotionState("focused", 0.81, "serious", "#9BC7FF")
        return EmotionState("calm", 0.73, "thinking", "#66CFFF")

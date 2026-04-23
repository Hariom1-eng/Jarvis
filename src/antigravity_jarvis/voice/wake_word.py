from antigravity_jarvis.config.settings import Settings


class WakeWordEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def listening_phrases(self) -> list[str]:
        return self.settings.assistant.wake_words

from antigravity_jarvis.config.settings import Settings


class TextToSpeechEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def speak(self, text: str, emotion: str) -> None:
        print(
            "[TTS]",
            {
                "voice": self.settings.voice.voice_profile,
                "emotion": emotion,
                "text": text,
            },
        )

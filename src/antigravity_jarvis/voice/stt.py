from antigravity_jarvis.config.settings import Settings


class SpeechToTextEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def transcribe(self, audio_bytes: bytes) -> str:
        del audio_bytes
        return "Transcription placeholder."

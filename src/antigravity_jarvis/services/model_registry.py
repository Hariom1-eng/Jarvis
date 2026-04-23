from dataclasses import dataclass

from antigravity_jarvis.config.settings import Settings


@dataclass(slots=True)
class ModelRegistry:
    primary_model: str
    coder_model: str
    embedding_model: str

    @classmethod
    def from_settings(cls, settings: Settings) -> "ModelRegistry":
        return cls(
            primary_model=settings.llm.primary_model,
            coder_model=settings.llm.coder_model,
            embedding_model=settings.llm.embedding_model,
        )

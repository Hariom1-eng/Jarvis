from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class UserTurn:
    text: str
    language: str = "en"
    source: str = "text"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class AssistantTurn:
    text: str
    mode: str
    emotion: str
    should_speak: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class EmotionState:
    label: str
    confidence: float
    avatar_expression: str
    glow_color: str

import json
from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class AssistantConfig:
    name: str
    default_mode: str
    wake_words: list[str]
    supported_languages: list[str]
    greeting_template: str
    greeting_enabled: bool = True


@dataclass(slots=True)
class RuntimeConfig:
    offline_required: bool
    low_ram_mode: bool
    gpu_enabled: bool
    max_context_messages: int
    ui_mode: str
    data_dir: str


@dataclass(slots=True)
class LLMConfig:
    provider: str
    endpoint: str
    primary_model: str
    coder_model: str
    embedding_model: str
    temperature: float


@dataclass(slots=True)
class MemoryConfig:
    provider: str
    persist_dir: str
    semantic_recall_limit: int


@dataclass(slots=True)
class VoiceConfig:
    wake_word_engine: str
    stt_engine: str
    tts_engine: str
    voice_profile: str
    interruptible: bool


@dataclass(slots=True)
class AvatarConfig:
    runtime: str
    transport: str
    endpoint: str
    style: str


@dataclass(slots=True)
class EmotionConfig:
    enabled: bool
    empathy_level: str


@dataclass(slots=True)
class SystemControlConfig:
    enabled: bool
    safe_mode: bool


@dataclass(slots=True)
class Settings:
    assistant: AssistantConfig
    runtime: RuntimeConfig
    llm: LLMConfig
    memory: MemoryConfig
    voice: VoiceConfig
    avatar: AvatarConfig
    emotion: EmotionConfig
    system_control: SystemControlConfig


def load_settings(config_path: Path | None = None) -> Settings:
    path = config_path or _default_config_path()
    payload = _load_payload(path)
    return Settings(
        assistant=AssistantConfig(**payload["assistant"]),
        runtime=RuntimeConfig(**payload["runtime"]),
        llm=LLMConfig(**payload["llm"]),
        memory=MemoryConfig(**payload["memory"]),
        voice=VoiceConfig(**payload["voice"]),
        avatar=AvatarConfig(**payload["avatar"]),
        emotion=EmotionConfig(**payload["emotion"]),
        system_control=SystemControlConfig(**payload["system_control"]),
    )


def _default_config_path() -> Path:
    json_path = Path("configs/default.json")
    yaml_path = Path("configs/default.yaml")
    if json_path.exists():
        return json_path
    return yaml_path


def _load_payload(path: Path) -> dict:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))

    try:
        import yaml  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "PyYAML is not installed and a YAML config was requested. "
            "Use configs/default.json or install the project dependencies."
        ) from exc

    return yaml.safe_load(path.read_text(encoding="utf-8"))

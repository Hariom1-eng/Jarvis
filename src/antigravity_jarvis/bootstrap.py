from pathlib import Path

from antigravity_jarvis.avatar.avatar_bridge import AvatarBridge
from antigravity_jarvis.brain.memory import MemoryEngine
from antigravity_jarvis.brain.session_manager import SessionManager
from antigravity_jarvis.config.settings import Settings, load_settings
from antigravity_jarvis.control.system_actions import SystemActionRegistry
from antigravity_jarvis.core.orchestrator import AssistantOrchestrator
from antigravity_jarvis.emotion.engine import EmotionEngine
from antigravity_jarvis.modes.router import ModeRouter
from antigravity_jarvis.planning.task_manager import TaskManager
from antigravity_jarvis.services.llm.runtime import LocalLLMRuntime
from antigravity_jarvis.services.model_registry import ModelRegistry
from antigravity_jarvis.ui.event_bus import UIEventBus
from antigravity_jarvis.voice.stt import SpeechToTextEngine
from antigravity_jarvis.voice.tts import TextToSpeechEngine
from antigravity_jarvis.voice.wake_word import WakeWordEngine


def create_assistant(config_path: Path | None = None) -> AssistantOrchestrator:
    settings: Settings = load_settings(config_path)
    model_registry = ModelRegistry.from_settings(settings)

    return AssistantOrchestrator(
        settings=settings,
        session_manager=SessionManager(),
        memory_engine=MemoryEngine(settings),
        emotion_engine=EmotionEngine(settings),
        llm_runtime=LocalLLMRuntime(settings, model_registry),
        mode_router=ModeRouter(settings),
        task_manager=TaskManager(settings),
        system_actions=SystemActionRegistry(),
        avatar_bridge=AvatarBridge(settings),
        wake_word_engine=WakeWordEngine(settings),
        stt_engine=SpeechToTextEngine(settings),
        tts_engine=TextToSpeechEngine(settings),
        ui_bus=UIEventBus(),
    )

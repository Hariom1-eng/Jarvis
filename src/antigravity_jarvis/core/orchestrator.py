from datetime import datetime

from antigravity_jarvis.api.schemas import AssistantTurn, UserTurn
from antigravity_jarvis.avatar.avatar_bridge import AvatarBridge
from antigravity_jarvis.brain.memory import MemoryEngine
from antigravity_jarvis.brain.session_manager import SessionManager
from antigravity_jarvis.config.settings import Settings
from antigravity_jarvis.control.system_actions import SystemActionRegistry
from antigravity_jarvis.emotion.engine import EmotionEngine
from antigravity_jarvis.modes.router import ModeRouter
from antigravity_jarvis.planning.task_manager import TaskManager
from antigravity_jarvis.services.llm.runtime import LocalLLMRuntime
from antigravity_jarvis.ui.event_bus import UIEventBus
from antigravity_jarvis.voice.stt import SpeechToTextEngine
from antigravity_jarvis.voice.tts import TextToSpeechEngine
from antigravity_jarvis.voice.wake_word import WakeWordEngine


class AssistantOrchestrator:
    def __init__(
        self,
        *,
        settings: Settings,
        session_manager: SessionManager,
        memory_engine: MemoryEngine,
        emotion_engine: EmotionEngine,
        llm_runtime: LocalLLMRuntime,
        mode_router: ModeRouter,
        task_manager: TaskManager,
        system_actions: SystemActionRegistry,
        avatar_bridge: AvatarBridge,
        wake_word_engine: WakeWordEngine,
        stt_engine: SpeechToTextEngine,
        tts_engine: TextToSpeechEngine,
        ui_bus: UIEventBus,
    ) -> None:
        self.settings = settings
        self.session_manager = session_manager
        self.memory_engine = memory_engine
        self.emotion_engine = emotion_engine
        self.llm_runtime = llm_runtime
        self.mode_router = mode_router
        self.task_manager = task_manager
        self.system_actions = system_actions
        self.avatar_bridge = avatar_bridge
        self.wake_word_engine = wake_word_engine
        self.stt_engine = stt_engine
        self.tts_engine = tts_engine
        self.ui_bus = ui_bus

    def boot(self) -> None:
        if self.settings.assistant.greeting_enabled:
            greeting = self._time_greeting()
            print(f"{self.settings.assistant.name}: {greeting}")
            self.ui_bus.publish("boot", greeting)

    def handle_text(self, text: str, language: str = "en") -> AssistantTurn:
        user_turn = UserTurn(text=text, language=language)
        self.session_manager.add_user_turn(user_turn)

        memory = self.memory_engine.recall(text)
        emotion = self.emotion_engine.detect(text)
        mode = self.mode_router.select_mode(text)
        reply = self._try_handle_builtin_commands(text, mode, emotion.label)
        if reply is None:
            reply = self.llm_runtime.generate(
                text=text,
                mode=mode,
                memory=memory,
                emotion=emotion.label,
                context=self.session_manager.recent_context(self.settings.runtime.max_context_messages),
            )

        assistant_turn = AssistantTurn(text=reply, mode=mode, emotion=emotion.label)
        self.session_manager.add_assistant_turn(assistant_turn)
        self.memory_engine.log_interaction(text, reply, mode, emotion.label)

        self.avatar_bridge.publish_state(
            expression=emotion.avatar_expression,
            speaking=True,
            glow_color=emotion.glow_color,
        )
        self.tts_engine.speak(reply, emotion.label)
        self.ui_bus.publish(
            "assistant_turn",
            {
                "text": assistant_turn.text,
                "mode": assistant_turn.mode,
                "emotion": assistant_turn.emotion,
            },
        )
        return assistant_turn

    def _try_handle_builtin_commands(self, text: str, mode: str, emotion: str) -> str | None:
        lowered = text.strip().lower()
        if lowered.startswith("remember that "):
            note = text.strip()[14:].strip()
            if note:
                self.memory_engine.remember(note)
                return f"Certainly sir. I have stored that in long-term memory: {note}"
        if lowered.startswith("remind me to "):
            reminder = text.strip()[13:].strip()
            if reminder:
                self.task_manager.add_reminder(reminder)
                return f"Certainly sir. Reminder stored: {reminder}"
        if lowered in {"show reminders", "what are my reminders", "list reminders"}:
            return f"Certainly sir. {self.task_manager.summary()}"
        if lowered in {"run diagnostics", "diagnostics", "system diagnostics"}:
            actions = ", ".join(action.name for action in self.system_actions.list_actions())
            return (
                "Running diagnostics. "
                f"Mode: {mode}. Emotion profile: {emotion}. "
                f"Registered local actions: {actions}. Task completed."
            )
        return None

    def _time_greeting(self) -> str:
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning sir. Systems online."
        if hour < 18:
            return "Good afternoon sir. Systems online."
        return "Good evening sir. Systems online."

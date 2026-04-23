import json
from urllib import error, request

from antigravity_jarvis.brain.memory import MemorySnapshot
from antigravity_jarvis.config.settings import Settings
from antigravity_jarvis.services.model_registry import ModelRegistry


class LocalLLMRuntime:
    """Placeholder runtime for local model providers.

    Replace this stub with a streaming Ollama or llama.cpp client in Phase 1.
    """

    def __init__(self, settings: Settings, registry: ModelRegistry) -> None:
        self.settings = settings
        self.registry = registry

    def generate(self, *, text: str, mode: str, memory: MemorySnapshot, emotion: str, context: list[object]) -> str:
        if self.settings.llm.provider.lower() == "ollama":
            remote = self._generate_with_ollama(text=text, mode=mode, memory=memory, emotion=emotion, context=context)
            if remote:
                return remote
        return self._fallback_response(text=text, mode=mode, memory=memory, emotion=emotion)

    def _generate_with_ollama(
        self,
        *,
        text: str,
        mode: str,
        memory: MemorySnapshot,
        emotion: str,
        context: list[object],
    ) -> str | None:
        prompt = self._build_prompt(text=text, mode=mode, memory=memory, emotion=emotion, context=context)
        payload = json.dumps(
            {
                "model": self.registry.primary_model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": self.settings.llm.temperature},
            }
        ).encode("utf-8")
        endpoint = self.settings.llm.endpoint.rstrip("/") + "/api/generate"
        req = request.Request(endpoint, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with request.urlopen(req, timeout=12) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (error.URLError, TimeoutError, json.JSONDecodeError):
            return None
        return body.get("response", "").strip() or None

    def _build_prompt(
        self,
        *,
        text: str,
        mode: str,
        memory: MemorySnapshot,
        emotion: str,
        context: list[object],
    ) -> str:
        recent = "\n".join(f"- {getattr(item, 'text', str(item))}" for item in context[-4:]) or "- No recent context"
        memories = "\n".join(f"- {note}" for note in memory.recalled_notes[:4]) or "- No relevant memories"
        return (
            "You are AntiGravity Jarvis, a premium fully offline desktop AI companion.\n"
            "Speak like a calm, intelligent, futuristic assistant.\n"
            "Use short polished replies, mild confidence, and selective Jarvis phrases such as "
            "'Certainly sir', 'Task completed', 'Running diagnostics', or 'I recommend caution' when natural.\n"
            f"Current mode: {mode}\n"
            f"Detected user emotion: {emotion}\n"
            "Supported languages include English, Hindi, and Urdu. Match the user naturally.\n"
            "Stay useful, concise, and action-oriented.\n\n"
            f"Relevant memory:\n{memories}\n\n"
            f"Recent context:\n{recent}\n\n"
            f"User request: {text}\n"
            "Assistant response:"
        )

    def _fallback_response(self, *, text: str, mode: str, memory: MemorySnapshot, emotion: str) -> str:
        recalled = "; ".join(memory.recalled_notes[:2]) or "no high-priority memory triggers"
        tone_line = {
            "concerned": "I recommend caution and a steady approach.",
            "celebratory": "This is a promising development.",
            "focused": "Running diagnostics on the request.",
            "calm": "Systems are stable.",
        }.get(emotion, "Systems are stable.")
        return (
            f"Certainly sir. {tone_line} "
            f"I am operating in {mode} mode with the local model path set to {self.registry.primary_model}. "
            f"Current recall: {recalled}. "
            f"For your request '{text}', the offline runtime fallback is active. Task completed."
        )

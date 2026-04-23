from dataclasses import dataclass, field
import json
from datetime import datetime
from pathlib import Path

from antigravity_jarvis.config.settings import Settings


@dataclass(slots=True)
class MemorySnapshot:
    profile_facts: list[str] = field(default_factory=list)
    recalled_notes: list[str] = field(default_factory=list)


class MemoryEngine:
    """Starter local memory layer.

    In production this should wrap a vector store plus structured profile storage.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.persist_dir = Path(settings.memory.persist_dir)
        if not self.persist_dir.is_absolute():
            self.persist_dir = Path(settings.runtime.data_dir) / self.persist_dir
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.profile_path = self.persist_dir / "profile.json"
        self.episodic_log_path = self.persist_dir / "episodic_log.jsonl"
        self.preferences_path = self.persist_dir / "preferences.json"

        self._profile_facts = self._load_profile_facts()

    def recall(self, query: str) -> MemorySnapshot:
        recalled = [fact for fact in self._profile_facts if any(word in fact.lower() for word in query.lower().split())]
        return MemorySnapshot(profile_facts=self._profile_facts[:], recalled_notes=recalled[:3])

    def remember(self, note: str) -> None:
        self._profile_facts.append(note)
        self._save_profile_facts()
        self._append_episode({"type": "memory_note", "note": note})

    def log_interaction(self, user_text: str, assistant_text: str, mode: str, emotion: str) -> None:
        self._append_episode(
            {
                "type": "interaction",
                "user_text": user_text,
                "assistant_text": assistant_text,
                "mode": mode,
                "emotion": emotion,
            }
        )

    def _load_profile_facts(self) -> list[str]:
        if self.profile_path.exists():
            payload = json.loads(self.profile_path.read_text(encoding="utf-8"))
            facts = payload.get("facts", [])
            if facts:
                return facts

        defaults = [
            "User prefers a premium Jarvis-like tone.",
            "Primary experience target is fully offline desktop usage.",
            "Assistant should feel like a calm futuristic desktop companion.",
        ]
        self.profile_path.write_text(json.dumps({"facts": defaults}, indent=2), encoding="utf-8")
        return defaults

    def _save_profile_facts(self) -> None:
        self.profile_path.write_text(json.dumps({"facts": self._profile_facts}, indent=2), encoding="utf-8")

    def _append_episode(self, event: dict[str, str]) -> None:
        payload = {
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            **event,
        }
        with self.episodic_log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")

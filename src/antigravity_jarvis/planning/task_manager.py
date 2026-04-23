import json
from pathlib import Path

from antigravity_jarvis.config.settings import Settings


class TaskManager:
    def __init__(self, settings: Settings) -> None:
        self.data_dir = Path(settings.runtime.data_dir) / "tasks"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.reminders_path = self.data_dir / "reminders.json"
        self.todos_path = self.data_dir / "todos.json"
        self.reminders = self._load_list(self.reminders_path)
        self.todos = self._load_list(self.todos_path)

    def add_reminder(self, reminder: str) -> None:
        self.reminders.append(reminder)
        self._save_list(self.reminders_path, self.reminders)

    def add_todo(self, item: str) -> None:
        self.todos.append(item)
        self._save_list(self.todos_path, self.todos)

    def summary(self) -> str:
        reminders = ", ".join(self.reminders[-3:]) if self.reminders else "no active reminders"
        todos = ", ".join(self.todos[-3:]) if self.todos else "no active tasks"
        return f"Reminders: {reminders}. Tasks: {todos}."

    def _load_list(self, path: Path) -> list[str]:
        if not path.exists():
            path.write_text("[]", encoding="utf-8")
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_list(self, path: Path, items: list[str]) -> None:
        path.write_text(json.dumps(items, indent=2), encoding="utf-8")

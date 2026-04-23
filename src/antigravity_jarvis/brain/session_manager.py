from dataclasses import dataclass, field

from antigravity_jarvis.api.schemas import AssistantTurn, UserTurn


@dataclass(slots=True)
class SessionManager:
    turns: list[object] = field(default_factory=list)

    def add_user_turn(self, turn: UserTurn) -> None:
        self.turns.append(turn)

    def add_assistant_turn(self, turn: AssistantTurn) -> None:
        self.turns.append(turn)

    def recent_context(self, limit: int = 8) -> list[object]:
        return self.turns[-limit:]

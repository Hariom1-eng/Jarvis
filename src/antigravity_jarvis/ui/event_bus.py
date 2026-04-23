from collections import defaultdict
from collections.abc import Callable


class UIEventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[object], None]]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[[object], None]) -> None:
        self._subscribers[event_name].append(callback)

    def publish(self, event_name: str, payload: object) -> None:
        print(f"[UIEventBus] {event_name}: {payload}")
        for callback in self._subscribers.get(event_name, []):
            callback(payload)

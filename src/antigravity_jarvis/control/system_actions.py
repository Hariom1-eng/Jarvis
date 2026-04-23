from dataclasses import dataclass


@dataclass(slots=True)
class SystemAction:
    name: str
    safety_level: str
    description: str


class SystemActionRegistry:
    def __init__(self) -> None:
        self._actions = {
            "open_app": SystemAction("open_app", "safe", "Open a desktop application."),
            "search_files": SystemAction("search_files", "safe", "Search local files."),
            "close_app": SystemAction("close_app", "confirm", "Close an application."),
            "run_script": SystemAction("run_script", "confirm", "Run a local automation script."),
        }

    def list_actions(self) -> list[SystemAction]:
        return list(self._actions.values())

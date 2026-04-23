from antigravity_jarvis.config.settings import Settings


class AvatarBridge:
    """Sends local animation and expression events to the avatar runtime."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def publish_state(self, expression: str, speaking: bool, glow_color: str) -> None:
        print(
            "[AvatarBridge]",
            {
                "expression": expression,
                "speaking": speaking,
                "glow_color": glow_color,
                "endpoint": self.settings.avatar.endpoint,
            },
        )

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from antigravity_jarvis.core.orchestrator import AssistantOrchestrator


STATIC_DIR = Path(__file__).with_name("web_static")


class JarvisWebApp:
    def __init__(self, assistant: AssistantOrchestrator) -> None:
        self.assistant = assistant
        self.last_boot_message = ""
        self.assistant.ui_bus.subscribe("boot", self._remember_boot)

    def _remember_boot(self, payload: object) -> None:
        self.last_boot_message = str(payload)

    def handle_boot(self) -> dict[str, str]:
        if not self.last_boot_message:
            self.assistant.boot()
        return {"message": self.last_boot_message}

    def handle_chat(self, message: str) -> dict[str, str]:
        turn = self.assistant.handle_text(message)
        return {
            "reply": turn.text,
            "mode": turn.mode,
            "emotion": turn.emotion,
        }

    def snapshot(self) -> dict[str, object]:
        return {
            "name": self.assistant.settings.assistant.name,
            "mode": self.assistant.settings.assistant.default_mode,
            "wake_words": self.assistant.wake_word_engine.listening_phrases(),
            "reminders": self.assistant.task_manager.reminders[-5:],
            "todos": self.assistant.task_manager.todos[-5:],
        }


def launch_localhost(assistant: AssistantOrchestrator, host: str = "127.0.0.1", port: int = 8000) -> None:
    web_app = JarvisWebApp(assistant)
    handler = _build_handler(web_app)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"AntiGravity Jarvis localhost control room running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAntiGravity Jarvis localhost server stopped.")
    finally:
        server.server_close()


def _build_handler(web_app: JarvisWebApp) -> type[BaseHTTPRequestHandler]:
    class JarvisHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            route = urlparse(self.path).path
            if route == "/":
                self._serve_file("index.html", "text/html; charset=utf-8")
                return
            if route == "/app.js":
                self._serve_file("app.js", "application/javascript; charset=utf-8")
                return
            if route == "/styles.css":
                self._serve_file("styles.css", "text/css; charset=utf-8")
                return
            if route == "/api/boot":
                self._send_json(web_app.handle_boot())
                return
            if route == "/api/state":
                self._send_json(web_app.snapshot())
                return
            self.send_error(HTTPStatus.NOT_FOUND, "Route not found")

        def do_POST(self) -> None:
            route = urlparse(self.path).path
            if route != "/api/chat":
                self.send_error(HTTPStatus.NOT_FOUND, "Route not found")
                return

            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            payload = json.loads(body)
            message = str(payload.get("message", "")).strip()
            if not message:
                self._send_json({"error": "Message is required."}, status=HTTPStatus.BAD_REQUEST)
                return
            self._send_json(web_app.handle_chat(message))

        def log_message(self, format: str, *args: object) -> None:
            return

        def _serve_file(self, file_name: str, content_type: str) -> None:
            file_path = STATIC_DIR / file_name
            if not file_path.exists():
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(file_path.read_bytes())

        def _send_json(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
            raw = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

    return JarvisHandler

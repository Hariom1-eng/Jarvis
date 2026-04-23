from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from antigravity_jarvis.core.orchestrator import AssistantOrchestrator


class JarvisDesktopApp:
    def __init__(self, assistant: AssistantOrchestrator) -> None:
        self.assistant = assistant
        self.root = tk.Tk()
        self.root.title("AntiGravity Jarvis")
        self.root.geometry("1220x760")
        self.root.configure(bg="#08111f")

        self.mode_var = tk.StringVar(value="Mode: professional")
        self.emotion_var = tk.StringVar(value="Emotion: calm")
        self.status_var = tk.StringVar(value="Status: systems ready")

        self._configure_styles()
        self._build_layout()
        self._bind_events()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Jarvis.TFrame", background="#08111f")
        style.configure("Card.TFrame", background="#0d1b2f")
        style.configure("Jarvis.TLabel", background="#08111f", foreground="#d9f6ff", font=("Segoe UI", 11))
        style.configure("Hero.TLabel", background="#08111f", foreground="#7be7ff", font=("Segoe UI Semibold", 22))
        style.configure("PanelTitle.TLabel", background="#0d1b2f", foreground="#7be7ff", font=("Segoe UI Semibold", 12))
        style.configure("Jarvis.TButton", background="#12304e", foreground="#dffcff", padding=8)

    def _build_layout(self) -> None:
        shell = ttk.Frame(self.root, style="Jarvis.TFrame", padding=18)
        shell.pack(fill="both", expand=True)

        header = ttk.Frame(shell, style="Jarvis.TFrame")
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="AntiGravity Jarvis", style="Hero.TLabel").pack(side="left")
        ttk.Label(header, textvariable=self.status_var, style="Jarvis.TLabel").pack(side="right")

        content = ttk.Frame(shell, style="Jarvis.TFrame")
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        left = ttk.Frame(content, style="Card.TFrame", padding=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right = ttk.Frame(content, style="Card.TFrame", padding=14)
        right.grid(row=0, column=1, sticky="nsew")

        ttk.Label(left, text="Conversation Console", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 10))
        self.chat = tk.Text(
            left,
            bg="#09101d",
            fg="#d9f6ff",
            insertbackground="#7be7ff",
            wrap="word",
            relief="flat",
            font=("Consolas", 11),
        )
        self.chat.pack(fill="both", expand=True)
        self.chat.configure(state="disabled")

        input_row = ttk.Frame(left, style="Card.TFrame")
        input_row.pack(fill="x", pady=(12, 0))
        self.prompt = tk.Text(
            input_row,
            height=4,
            bg="#0b1628",
            fg="#f4fdff",
            insertbackground="#7be7ff",
            relief="flat",
            font=("Segoe UI", 11),
        )
        self.prompt.pack(fill="x", expand=True, side="left")
        send_button = ttk.Button(input_row, text="Send", style="Jarvis.TButton", command=self._send_prompt)
        send_button.pack(side="left", padx=(10, 0))

        ttk.Label(right, text="Command Center", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 12))
        self._panel_label(right, self.mode_var)
        self._panel_label(right, self.emotion_var)
        self._panel_label(right, self.status_var)

        self.metrics = tk.Text(
            right,
            height=20,
            bg="#09101d",
            fg="#9eefff",
            relief="flat",
            wrap="word",
            font=("Consolas", 10),
        )
        self.metrics.pack(fill="both", expand=True, pady=(10, 0))
        self.metrics.insert(
            "end",
            "Jarvis HUD initialized.\n"
            "- Offline brain: ready\n"
            "- Voice pipeline: placeholder connected\n"
            "- Avatar bridge: local event mode\n"
            "- Memory core: persistent\n"
            "- Suggested first commands:\n"
            "  remember that my favorite IDE is VS Code\n"
            "  remind me to review the roadmap\n"
            "  run diagnostics\n",
        )
        self.metrics.configure(state="disabled")

    def _panel_label(self, parent: ttk.Frame, variable: tk.StringVar) -> None:
        label = ttk.Label(parent, textvariable=variable, style="Jarvis.TLabel")
        label.pack(anchor="w", pady=4)

    def _bind_events(self) -> None:
        self.assistant.ui_bus.subscribe("boot", self._on_boot)
        self.assistant.ui_bus.subscribe("assistant_turn", self._on_assistant_turn)
        self.root.bind("<Control-Return>", lambda event: self._send_prompt())
        self.root.after(100, self.assistant.boot)

    def _send_prompt(self) -> None:
        text = self.prompt.get("1.0", "end").strip()
        if not text:
            return
        self.prompt.delete("1.0", "end")
        self._append_chat("You", text)
        self.status_var.set("Status: processing request")
        threading.Thread(target=self._run_turn, args=(text,), daemon=True).start()

    def _run_turn(self, text: str) -> None:
        turn = self.assistant.handle_text(text)
        self.root.after(
            0,
            lambda: (
                self.mode_var.set(f"Mode: {turn.mode}"),
                self.emotion_var.set(f"Emotion: {turn.emotion}"),
                self.status_var.set("Status: response complete"),
            ),
        )

    def _append_chat(self, speaker: str, text: str) -> None:
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{speaker}: {text}\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def _on_boot(self, greeting: object) -> None:
        self.root.after(0, lambda: self._append_chat("Jarvis", str(greeting)))

    def _on_assistant_turn(self, payload: object) -> None:
        if isinstance(payload, dict):
            text = str(payload.get("text", ""))
            mode = str(payload.get("mode", "professional"))
            emotion = str(payload.get("emotion", "calm"))
        else:
            text = str(payload)
            mode = "professional"
            emotion = "calm"

        def update() -> None:
            self._append_chat("Jarvis", text)
            self.mode_var.set(f"Mode: {mode}")
            self.emotion_var.set(f"Emotion: {emotion}")

        self.root.after(0, update)

    def run(self) -> None:
        self.root.mainloop()


def launch_desktop(assistant: AssistantOrchestrator) -> None:
    app = JarvisDesktopApp(assistant)
    app.run()

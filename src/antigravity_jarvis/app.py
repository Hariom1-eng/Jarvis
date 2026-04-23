import argparse

from antigravity_jarvis.bootstrap import create_assistant
from antigravity_jarvis.ui.desktop import launch_desktop
from antigravity_jarvis.ui.web import launch_localhost


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AntiGravity Jarvis offline desktop assistant")
    parser.add_argument("--cli", action="store_true", help="Run in terminal mode.")
    parser.add_argument("--web", action="store_true", help="Run a localhost web control room.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface for web mode.")
    parser.add_argument("--port", type=int, default=8000, help="Port for web mode.")
    parser.add_argument("--prompt", help="Send a single prompt and print the reply.")
    return parser


def run_cli() -> None:
    assistant = create_assistant()
    assistant.boot()
    while True:
        try:
            text = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAntiGravity Jarvis: Shutting down cleanly, sir.")
            break
        if not text:
            continue
        if text.lower() in {"exit", "quit"}:
            print("AntiGravity Jarvis: Until next time, sir.")
            break
        turn = assistant.handle_text(text)
        print(f"AntiGravity Jarvis> {turn.text}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    assistant = create_assistant()

    if args.prompt:
        assistant.boot()
        turn = assistant.handle_text(args.prompt)
        print(turn.text)
        return

    if args.cli:
        run_cli()
        return

    if args.web:
        launch_localhost(assistant, host=args.host, port=args.port)
        return

    if assistant.settings.runtime.ui_mode == "localhost":
        launch_localhost(assistant, host=args.host, port=args.port)
        return

    launch_desktop(assistant)


if __name__ == "__main__":
    main()

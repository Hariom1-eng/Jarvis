# Setup Guide

## Goal

This setup is designed so the assistant works without internet after installation and model download are complete.

## Phase 1 Setup Stack

- Python 3.11+
- Ollama or llama.cpp server for local LLM inference
- faster-whisper or whisper.cpp for STT
- Piper for TTS
- PySide6 for desktop UI
- Unity for the 3D avatar runtime

## Windows Setup Steps

### 1. Create a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[desktop,local-llm,voice,tts,memory,automation]
```

### 2. Install a Local LLM Runtime

Recommended first choice:

- Install Ollama locally
- Pull models while internet is available

Example:

```powershell
ollama pull qwen2.5:7b-instruct
ollama pull deepseek-coder:6.7b
ollama pull nomic-embed-text
```

Alternative:

- Use llama.cpp server with quantized GGUF models stored locally

### 3. Prepare Voice Assets

- Download Whisper model files
- Download Piper voice files
- Store them under a local `models/` directory outside version control

Suggested layout:

```text
models/
├─ llm/
├─ stt/
├─ tts/
└─ wakeword/
```

### 4. Configure the Assistant

- Copy `configs/default.yaml`
- Adjust model names, endpoints, and performance flags
- Set low-RAM mode if needed

### 5. Launch the Starter App

```powershell
jarvis
```

## Avatar Setup

### Recommended Path

Use Unity as a sidecar app that:

- loads a humanoid avatar
- receives animation and speech cues from Python
- renders facial expressions and hologram effects

### Unity Requirements

- Humanoid rig with blend shapes
- lip sync support
- animation controller for idle, thinking, speaking, greeting
- local WebSocket client/server bridge
- emissive hologram shader with mood-linked color states

## Packaging Strategy

When moving toward a real desktop product:

- package Python backend with PyInstaller
- distribute model assets separately or via first-run installer
- ship Unity avatar runtime as a bundled companion executable
- use an installer that validates GPU drivers and disk space

## Offline Guarantee Checklist

Before declaring the product offline-ready, verify:

- LLM runs locally with no remote API fallback
- STT works with network disabled
- TTS works with network disabled
- wake word works with network disabled
- memory and reminders persist locally
- avatar animations do not depend on cloud assets

## Suggested MVP Milestone

Ship this first:

1. Offline chat and voice
2. Jarvis persona modes
3. Local memory
4. Desktop dashboard
5. Safe system controls
6. Placeholder avatar bridge

Then add the full 3D layer after the core intelligence feels solid.

# Recommended Models

## Primary Assistant Models

These are strong local options for an offline Jarvis-style assistant.

### Balanced Default

- `Qwen2.5 7B Instruct`
  - Best overall balance of reasoning, multilingual quality, and speed
  - Strong for English, decent for Hindi and Urdu support
  - Good default for chat, planning, and general assistance

### Premium Local Upgrade

- `Qwen2.5 14B Instruct`
  - Better reasoning and tone control
  - Better for longer context and more sophisticated conversations
  - Best on systems with strong GPUs and at least 16 GB VRAM or high-RAM CPU setups

### Coding-Focused Side Model

- `DeepSeek Coder 6.7B`
  - Strong coding support
  - Useful for Hacker Mode, Engineer Mode, and automation script generation

### Low-RAM Fallback

- `Phi-3 Mini`
  - Lightweight and responsive
  - Good for lower-end or battery-sensitive sessions

## Speech Models

### Offline STT

- `faster-whisper`
  - Recommended model sizes:
    - `small` for mid-range hardware
    - `medium` for higher accuracy

- `whisper.cpp`
  - Strong alternative when you want extremely portable local deployment

### Offline TTS

- `Piper`
  - Fast, local, low-latency
  - Best for practical first release

- `Coqui XTTS`
  - Better expressiveness if you can accept heavier local runtime costs

## Wake Word

- `openWakeWord`
  - Lightweight and practical
  - Supports custom wake phrases like `Hey Jarvis` and `AntiGravity`

## Embeddings for Memory

- `nomic-embed-text`
  - Reliable for local semantic memory

- `bge-small-en-v1.5`
  - Great lightweight fallback for English-heavy usage

## Mood and Emotion

Start simple:

- Use rule-based and LLM-assisted sentiment classification locally
- Later add a lightweight audio emotion model for voice prosody cues

## Suggested Hardware Tiers

### Mid-Range PC

- Main model: `Qwen2.5 7B Instruct`
- STT: `faster-whisper small`
- TTS: `Piper`
- Avatar: medium-fidelity real-time shaders and optimized blend shapes

### Strong Enthusiast PC

- Main model: `Qwen2.5 14B Instruct`
- Coding model: `DeepSeek Coder 6.7B`
- STT: `faster-whisper medium`
- TTS: `Piper` or `Coqui XTTS`
- Avatar: higher-fidelity facial rig and richer post-processing

## Routing Strategy

Use model routing instead of forcing one model to do everything:

- General chat: `Qwen2.5 7B/14B`
- Coding: `DeepSeek Coder`
- Memory embeddings: `nomic-embed-text`
- Low-RAM mode: `Phi-3 Mini`

This improves speed and keeps the offline experience practical.

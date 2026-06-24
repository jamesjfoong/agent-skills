---
name: whisper
description: "Transcribe audio/video recordings using OpenAI Whisper locally. Trigger when the user wants to transcribe a meeting, convert speech to text, or extract transcripts from audio/video files."
---

# Whisper — Local Audio Transcription

Transcribe audio and video files using OpenAI Whisper locally. No cloud upload.

## Install

```bash
# System deps (ffmpeg required)
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg

# Option 1: pip in venv (recommended)
python3 -m venv /tmp/whisper_env
/tmp/whisper_env/bin/pip install openai-whisper

# Option 2: system-wide (override PEP 668 block)
pip3 install --break-system-packages openai-whisper
```

## Models

 whisper downloads models automatically on first use to `~/.cache/whisper/`:

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| `tiny` | 39 MB | fastest | testing/demo |
| `base` | 74 MB | fast | quick drafts |
| `small` | 244 MB | medium | default balance |
| `medium` | 769 MB | slow | accuracy |
| `large` | 1550 MB | slowest | best accuracy |

Set custom cache dir: `--model_dir /path/to/cache`

## Basic Transcription

```bash
# CLI direct
whisper /path/to/recording.mp3 --model small --language English --output_dir ./transcripts

# Via venv
/tmp/whisper_env/bin/whisper /path/to/recording.wav --model base --language English --output_dir /tmp
```

## Output Formats

```bash
# Single format
whisper audio.wav --output_format txt

# All formats at once
whisper audio.wav --output_format all
```

Supported: `txt`, `vtt`, `srt`, `tsv`, `json`, `all`

## Python API

```python
import whisper, json

model = whisper.load_model("small", download_root="~/.cache/whisper")
result = model.transcribe("/path/to/audio.wav", language="en")

# Raw text
with open("transcript.txt", "w") as f:
    f.write(result["text"])

# Full segments with timestamps
with open("transcript.json", "w") as f:
    json.dump(result, f)
```

## Common Options

```bash
whisper audio.wav \
  --model small \
  --language English \
  --output_dir ./out \
  --output_format all \
  --verbose False \
  --task transcribe    # or translate (to English)
```

## Workflow Tips

1. **Audio prep**: Whisper handles mp3, wav, m4a, mkv. For tricky files:
   ```bash
   ffmpeg -i recording.mkv -vn -acodec pcm_s16le -ar 16000 -ac 1 out.wav
   ```

2. **Google Drive → local**: Use `gogcli` skill to pull files first:
   ```bash
   gog drive download <fileId> --out /tmp/recording
   ```

3. **CPU limitation**: No GPU → use `base` model for speed. Small on ~30min takes ~8min CPU. Large can take hours.

4. **FP16 warning on CPU**: Harmless. Automatically falls back to FP32.

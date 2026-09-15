# gradium-tts

Convert text to speech using Gradium's Text-to-Speech API and play the audio output.

## When to use

- User wants to hear text read aloud
- User wants to convert text to speech
- User wants to generate audio from text

## Setup

1. Install the venv dependencies (done on first run):
```bash
python3 -m venv venv && ./venv/bin/pip install gradium soundfile sounddevice numpy
```

2. Create a `.env` file with your Gradium API key:
```
GRADIUM_API_KEY=your_api_key_here
```

Get your key from https://docs.gradium.ai

## Usage

Run the TTS app:
```bash
./venv/bin/python tts.py "Hello, world!"
./venv/bin/python tts.py "Hello, world!" -o output.wav
./venv/bin/python tts.py -v "YTpq7expH9539ERJ" "Say this with a different voice"
./venv/bin/python tts.py --help
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o OUTPUT` | Save to WAV file (plays + saves) | plays only |
| `-v VOICE` | Voice ID (see below) | flagship voice |
| `-r RATE` | Playback sample rate | 48000 |

### Available Voices

Check the Gradium docs at https://docs.gradium.ai/guides/voices/overview for the full list of voice IDs.

## How it works

The app reads the `.env` file for the Gradium API key, then uses the `gradium` Python SDK to call the TTS API. The resulting WAV audio is either played via `sounddevice` or saved to a file.

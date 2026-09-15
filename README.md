# Gradium TTS OpenClaw Skill

Text-to-Speech skill for OpenClaw powered by [Gradium](https://docs.gradium.ai/)'s low-latency TTS API.

## Features

- Convert any text to natural-sounding speech
- Stream audio output in real-time
- Save audio as WAV files
- Plug-and-play with OpenClaw skills system

## Quick Start

```bash
# Install dependencies
python3 -m venv venv && ./venv/bin/pip install gradium soundfile sounddevice numpy

# Create env file
echo "GRADIUM_API_KEY=your_key_here" > .env

# Run it
./venv/bin/python tts.py "Hello, world!"
./venv/bin/python tts.py -o greeting.wav "Hello, world!"
```

## Get an API Key

Sign up at [Gradium](https://docs.gradium.ai/) and get your API key.

## License

MIT

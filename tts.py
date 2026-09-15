#!/usr/bin/env python3
"""Gradium TTS app — convert text to speech and play it."""

import os
import sys
import asyncio
import argparse

# Add venv site-packages so gradium/soundfile can be found
venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
if os.path.exists(venv_path):
    sys.path.insert(0, os.path.join(venv_path, "lib", "python3.12", "site-packages"))

# Load env file if present
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

if not os.environ.get("GRADIUM_API_KEY"):
    print("Error: set GRADIUM_API_KEY environment variable", file=sys.stderr)
    sys.exit(1)


try:
    import soundfile as sf
    import numpy as np
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False


async def main():
    import gradium

    parser = argparse.ArgumentParser(description="Gradium TTS")
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("-o", "--output", "-f", help="Save to WAV file")
    parser.add_argument("-v", "--voice", default="YTpq7expH9539ERJ", help="Voice ID (default: flagship voice)")
    parser.add_argument("-r", "--rate", type=int, default=48000, help="Playback sample rate")
    args = parser.parse_args()

    print(f'TTS: "{args.text[:60]}..."', file=sys.stderr)
    print("Generating speech...", file=sys.stderr)

    client = gradium.client.GradiumClient()
    result = await client.tts(
        setup={"voice_id": args.voice, "output_format": "wav"},
        text=args.text,
    )

    raw = result.raw_data

    if args.output:
        with open(args.output, "wb") as f:
            f.write(raw)
        print(f"Saved to {args.output}", file=sys.stderr)

    # Try to play
    if HAS_SOUNDFILE:
        try:
            import sounddevice as sd
            arr = np.frombuffer(raw, dtype=np.int16)
            sd.play(arr, samplerate=args.rate)
            sd.wait()
            print("Played audio.", file=sys.stderr)
        except Exception as e:
            print(f"Could not play audio: {e}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())

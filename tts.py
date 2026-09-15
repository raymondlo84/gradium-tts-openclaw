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
    import sounddevice as sd
    import gradium

    parser = argparse.ArgumentParser(description="Gradium TTS")
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("-o", "--output", "-f", help="Save to WAV file")
    parser.add_argument("-v", "--voice", default="YTpq7expH9539ERJ", help="Voice ID (default: flagship voice)")
    parser.add_argument("-r", "--rate", type=int, default=48000, help="Playback sample rate")
    parser.add_argument("-d", "--device", type=int, default=None, help="Audio device index (default: system default)")
    parser.add_argument("--list-devices", action="store_true", help="List all audio devices and exit")
    args = parser.parse_args()

    # List devices if requested
    if args.list_devices:
        print("=== Audio Devices ===", file=sys.stderr)
        for i in range(sd.query_devices().__len__()):
            try:
                d = sd.query_devices(i)
                name = d["name"]
                inp = d.get("max_input_channels", 0)
                outp = d.get("max_output_channels", 0)
                rate = d.get("default_samplerate", "?")
                print(f"  [{i}] {name} (in:{inp} out:{outp} {rate}Hz)", file=sys.stderr)
            except Exception:
                pass
        return

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
            # Check if PipeWire is available and use it as default backend
            # This properly exposes USB devices like Zone Vibe 130
            use_pipewire = False
            try:
                import subprocess
                result = subprocess.run(['pactl', 'info'], capture_output=True, text=True, timeout=5)
                if 'PipeWire' in result.stdout or 'pipewire' in result.stdout:
                    use_pipewire = True
            except Exception:
                pass
            
            # Override device if specified
            if args.device is not None:
                sd.default.device = (args.device, args.device)
                dev_name = f"device {args.device}"
            elif use_pipewire:
                # Use pipewire as default backend for proper device detection
                sd.default.device = ('pipewire', 'pipewire')
                dev_name = "PipeWire (pipewire)"
            else:
                dev_idx = sd.default.device[0] if isinstance(sd.default.device, (list, tuple)) else sd.default.device
                try:
                    dev_name = sd.query_devices(dev_idx)["name"]
                except Exception:
                    dev_name = f"device index {dev_idx}"
            
            arr = np.frombuffer(raw, dtype=np.int16)
            print(f"Playing through: {dev_name}", file=sys.stderr)
            sd.play(arr, samplerate=args.rate)
            sd.wait()
            print("Done.", file=sys.stderr)
        except Exception as e:
            print(f"Could not play audio: {e}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())

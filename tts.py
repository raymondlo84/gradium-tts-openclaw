#!/usr/bin/env python3
"""Gradium TTS - Convert text to speech and play audio or save to WAV."""

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description="Gradium TTS - Text to Speech")
    parser.add_argument("text", nargs="?", default=None, help="Text to convert to speech")
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Save to WAV file (also plays)"
    )
    parser.add_argument("-v", "--voice", type=str, default=None, help="Voice ID")
    parser.add_argument(
        "-r", "--rate", type=int, default=48000, help="Playback sample rate (default: 48000)"
    )
    args = parser.parse_args()

    # Load environment variables from .env file
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)

    api_key = os.environ.get("GRADIUM_API_KEY")
    if not api_key:
        print("Error: GRADIUM_API_KEY not set. Create a .env file with your API key.", file=sys.stderr)
        sys.exit(1)

    if not args.text:
        parser.print_help()
        print("\nError: Please provide text to convert.", file=sys.stderr)
        sys.exit(1)

    # Import gradium after validation
    try:
        import gradium
    except ImportError:
        print(
            "Error: 'gradium' package not installed. Install with: "
            "pip install gradium soundfile sounddevice numpy",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Generating speech: {args.text[:60]}{'...' if len(args.text) > 60 else ''}")

    # Call Gradium TTS API
    client = gradium.Gradium(api_key=api_key)

    try:
        response = client.tts(
            text=args.text,
            voice_id=args.voice,  # type: ignore
            sample_rate=args.rate,
        )

        # response should contain audio data - adapt based on actual gradium API
        # This is a placeholder for the actual gradium SDK response handling
        audio_data = response.audio if hasattr(response, "audio") else response
        sample_rate = response.sample_rate if hasattr(response, "sample_rate") else args.rate

        if isinstance(audio_data, np.ndarray):
            audio_array = audio_data
        elif isinstance(audio_data, (list, bytes)):
            audio_array = np.array(audio_data, dtype=np.float32)
        else:
            print(f"Unexpected audio data type: {type(audio_data)}", file=sys.stderr)
            sys.exit(1)

        # Play audio
        print("Playing audio...")
        sd.play(audio_array, samplerate=sample_rate)
        sd.wait()

        # Save to file if requested
        if args.output:
            sf.write(args.output, audio_array, sample_rate)
            print(f"Audio saved to: {args.output}")

        print("Done!")

    except Exception as e:
        print(f"Error during TTS generation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Gradium Speech Plugin for OpenClaw

Gradium is an official OpenClaw TTS plugin. This is the recommended approach for integrating Gradium text-to-speech directly into your OpenClaw Gateway — it replaces manual `tts.py` calls with automatic speech synthesis on every text reply.

## Install Plugin

```bash
openclaw plugins install @openclaw/gradium-speech
```

The installation applies to a running Gateway automatically, or takes effect on the next startup.

## Setup

### 1. Get an API Key

Create a Gradium account and API key at [https://gradium.ai](https://gradium.ai).

### 2. Configure the Plugin

Expose your API key via environment variable or gateway config. Config takes precedence over the env var.

**Via environment variable:**

```bash
export GRADIUM_API_KEY="your-gradium-api-key"
```

**Via gateway config (`openclaw.json`):**
Copy and paste this to the bottom 
```json5
  "tts": {
    "auto": "always",
    "provider": "gradium",
    "providers": {
      "gradium": {
        "speakerVoiceId": "YTpq7expH9539ERJ",
        "apiKey": "REPLACE_THIS_WITH_API_KEY"
      }
    }
  }

```

| Key | Type | Description |
| --- | --- | --- |
| `tts.providers.gradium.apiKey` | string | Resolved API key. Supports `${ENV}` and secret refs. |
| `tts.providers.gradium.baseUrl` | string | HTTPS Gradium API URL on `api.gradium.ai`. Trailing slashes stripped. Default `https://api.gradium.ai`. |
| `tts.providers.gradium.speakerVoiceId` | string | Default voice id used when no directive override is present. |

Output format is chosen automatically by the target surface (see [Output](#output)) and is not configurable in `openclaw.json`.

## Voices

| Name | Voice ID |
| --- | --- |
| Arthur | `3jUdJyOi9pgbxBTK` |
| Christina | `2H4HY2CBNyJHBCrP` |
| Emma **(default)** | `YTpq7expH9539ERJ` |
| John | `KWJiFWu2O9nMPYcR` |
| Kent | `LFZvm12tW_z0xfGo` |
| Sydney | `jtEKaLYNn6iif5PR` |
| Tiffany | `Eu9iL_CYe8N-Gkx_` |

### Per-message voice override

When the active speech policy allows voice overrides, switch voices inline with a directive token:

```text
/voice:LFZvm12tW_z0xfGo
/voice_id:LFZvm12tW_z0xfGo
/voiceid:LFZvm12tW_z0xfGo
/gradium_voice:LFZvm12tW_z0xfGo
/gradiumvoice:LFZvm12tW_z0xfGo
```

If the speech policy disables voice overrides, the directive is consumed but ignored.

## Output

Output format is selected by target surface; the provider does not synthesize other formats.

| Target | Format | File ext | Sample rate | Voice-compatible flag |
| --- | --- | --- | --- | --- |
| Standard audio | `wav` | `.wav` | provider | no |
| Voice note | `opus` | `.opus` | provider | yes |
| Telephony | `ulaw_8000` | n/a | 8 kHz | n/a |

## Auto-select

Among configured TTS providers, Gradium's auto-select order is `30`. See [Text-to-Speech](https://docs.openclaw.ai/tools/tts) for how OpenClaw picks the active provider when `tts.provider` is not pinned.

## Relation to This Repo

This repo (`gradium-tts-openclaw`) contains a standalone Python-based TTS CLI (`tts.py`) that you can use independently of the OpenClaw plugin. The plugin approach above integrates Gradium directly into OpenClaw's native TTS system, so all text replies are automatically spoken.

If you're using the plugin, you typically don't need the standalone `tts.py` script — OpenClaw handles everything. But you can still use the Python CLI for offline generation, batch processing, or when you want more control over audio parameters.

## Related

- [Gradium Provider Docs](https://docs.openclaw.ai/providers/gradium)
- [Text-to-Speech](https://docs.openclaw.ai/tools/tts)
- [Media Overview](https://docs.openclaw.ai/tools/media-overview)

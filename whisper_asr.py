import os

import av

_original_av_open = av.open


def _compat_av_open(*args, **kwargs):
    kwargs.pop("metadata_errors", None)
    return _original_av_open(*args, **kwargs)


av.open = _compat_av_open

from faster_whisper import WhisperModel

# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(PROJECT_DIR, "audio", "new_stutter.mp3")

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# LOAD WHISPER MODEL
# ============================================================

print("=" * 70)
print("FASTER-WHISPER ASR")
print("=" * 70)

print("\nLoading Whisper model...")

# "tiny" is fastest and suitable for testing
# We can later use "base" for the final experiment

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded successfully.")

# ============================================================
# TRANSCRIPTION
# ============================================================

print("\nTranscribing audio...")

segments, info = model.transcribe(
    AUDIO_PATH,
    language="en",
    beam_size=5
)

# ============================================================
# COLLECT SEGMENTS
# ============================================================

transcription_parts = []

for segment in segments:

    text = segment.text.strip()

    print(
        f"[{segment.start:.2f}s - "
        f"{segment.end:.2f}s] {text}"
    )

    transcription_parts.append(text)

transcription = " ".join(
    transcription_parts
).strip()

# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 70)
print("WHISPER TRANSCRIPTION")
print("=" * 70)

print("\n" + transcription)

# ============================================================
# AUDIO INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("AUDIO INFORMATION")
print("=" * 70)

print(f"Detected language: {info.language}")
print(f"Language probability: {info.language_probability:.2f}")

# ============================================================
# SAVE TRANSCRIPTION
# ============================================================

output_file = os.path.join(
    OUTPUT_DIR,
    "whisper_transcription.txt"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(transcription)

print(
    f"\nTranscription saved to: {output_file}"
)
import os
import torch
import librosa

from transformers import (
    Wav2Vec2Processor,
    Wav2Vec2ForCTC
)

# ============================================================
# CONFIGURATION
# ============================================================

AUDIO_PATH = r"D:\new_stutter.mp3"

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "facebook/wav2vec2-base-960h"

print("=" * 70)
print("WAV2VEC2 ASR")
print("=" * 70)

print("\nLoading processor...")

processor = Wav2Vec2Processor.from_pretrained(
    MODEL_NAME
)

print("Loading ASR model...")

model = Wav2Vec2ForCTC.from_pretrained(
    MODEL_NAME
)

# ============================================================
# LOAD AUDIO
# ============================================================

print("\nLoading audio...")

audio, sample_rate = librosa.load(
    AUDIO_PATH,
    sr=16000,
    mono=True
)

print(f"Audio sample rate: {sample_rate} Hz")
print(f"Audio duration   : {len(audio) / sample_rate:.2f} seconds")

# ============================================================
# PREPARE AUDIO
# ============================================================

input_values = processor(
    audio,
    sampling_rate=16000,
    return_tensors="pt"
).input_values

print("\nInput tensor shape:")
print(input_values.shape)

# ============================================================
# ASR INFERENCE
# ============================================================

print("\nRunning speech recognition...")

with torch.no_grad():

    logits = model(
        input_values
    ).logits

# ============================================================
# CTC DECODING
# ============================================================

predicted_ids = torch.argmax(
    logits,
    dim=-1
)

transcription = processor.batch_decode(
    predicted_ids
)[0]

# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 70)
print("ASR RESULT")
print("=" * 70)

print("\nRecognized text:")
print(transcription)

# ============================================================
# SAVE RESULT
# ============================================================

output_file = os.path.join(
    OUTPUT_DIR,
    "asr_transcription.txt"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    f.write("ASR Transcription\n")
    f.write("=================\n\n")
    f.write(transcription)

print(
    f"\nTranscription saved to: {output_file}"
)
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(PROJECT_DIR, "audio", "new_stutter.mp3")

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# LOAD AUDIO
# ============================================================

audio, sample_rate = librosa.load(
    AUDIO_PATH,
    sr=None,
    mono=True
)

duration = len(audio) / sample_rate

print("=" * 65)
print("VOICE - TEXT - SPEECH PROJECT")
print("=" * 65)

print(f"Audio file : {AUDIO_PATH}")
print(f"Sample rate: {sample_rate} Hz")
print(f"Duration   : {duration:.2f} seconds")
print(f"Samples    : {len(audio)}")

# ============================================================
# WAVEFORM
# ============================================================

time = librosa.times_like(
    audio,
    sr=sample_rate
)

plt.figure(figsize=(14, 5))

plt.plot(time, audio)

plt.title("Waveform of Stuttered Speech")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")

plt.tight_layout()

waveform_path = os.path.join(
    OUTPUT_DIR,
    "waveform.png"
)

plt.savefig(
    waveform_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(f"\nWaveform saved to: {waveform_path}")

# ============================================================
# MEL SPECTROGRAM
# ============================================================

mel_spectrogram = librosa.feature.melspectrogram(
    y=audio,
    sr=sample_rate,
    n_mels=128,
    n_fft=2048,
    hop_length=512
)

# ============================================================
# CONVERT TO LOG SCALE
# ============================================================

log_mel_spectrogram = librosa.power_to_db(
    mel_spectrogram,
    ref=np.max
)

# ============================================================
# DISPLAY LOG-MEL SPECTROGRAM
# ============================================================

plt.figure(figsize=(14, 6))

librosa.display.specshow(
    log_mel_spectrogram,
    sr=sample_rate,
    hop_length=512,
    x_axis="time",
    y_axis="mel"
)

plt.colorbar(
    format="%+2.0f dB"
)

plt.title("Log-Mel Spectrogram of Stuttered Speech")
plt.xlabel("Time (seconds)")
plt.ylabel("Mel Frequency")

plt.tight_layout()

spectrogram_path = os.path.join(
    OUTPUT_DIR,
    "log_mel_spectrogram.png"
)

plt.savefig(
    spectrogram_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(
    f"Log-Mel spectrogram saved to: {spectrogram_path}"
)

# ============================================================
# FEATURE INFORMATION
# ============================================================

print("\n" + "=" * 65)
print("FEATURE EXTRACTION")
print("=" * 65)

print(
    f"Mel feature shape: {log_mel_spectrogram.shape}"
)

print(
    "The Log-Mel spectrogram represents "
    "the frequency characteristics of speech over time."
)
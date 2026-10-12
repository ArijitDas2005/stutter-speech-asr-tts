# Stutter Speech ASR and TTS

A Python project demonstrating a speech-processing pipeline for a sample with speech disfluencies:

**Speech → feature extraction → log-Mel spectrum → ASR → CTC → text → TTS → speech**

It creates waveform and log-Mel visualizations, compares Wav2Vec2 and Whisper transcription, demonstrates CTC decoding, calculates word error rate (WER), and synthesizes speech from a transcript. This is an educational demonstration, not a clinical assessment or diagnostic tool.

## Repository contents

- `main.py` — waveform and log-Mel spectrogram generation
- `asr.py` — Wav2Vec2-base-960h transcription with CTC decoding
- `whisper_asr.py` — Whisper-base transcription
- `ctc_demo.py` — small CTC greedy-decoding example
- `wer.py` — compares both ASR outputs with a reference transcript
- `tts.ps1` — synthesizes the Whisper transcript using Windows speech synthesis
- `stutter_speech_pipeline.ipynb` — notebook workflow for local use or Google Colab
- `report/` — mini-report, architecture diagram, and three-minute demo script
- `audio/new_stutter.mp3` — source audio used for the included example
- `outputs/` — waveform and spectrogram figures, ASR transcripts, WER reference/results, and synthesized TTS audio

**Audio privacy:** This public repository includes a voice recording, transcripts, and synthesized speech derived from it. Share or reuse these files only with the speaker's informed permission and any required rights. The recording is provided for this demonstration; do not assume it is cleared for unrelated reuse.

## Requirements

- Python 3.10 or later (the notebook can also run in Google Colab)
- Windows PowerShell for `tts.ps1`; the notebook TTS cell uses gTTS and needs internet access
- The included source audio file at `audio/new_stutter.mp3`. Replace that file to use another recording.

Install Python dependencies in a virtual environment:

```powershell
Set-Location "D:\path\to\stutter-speech-asr-tts"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Generate project outputs

Run the scripts in order:

```powershell
python main.py
python asr.py
python whisper_asr.py
```

For WER, create `outputs\reference_transcript.txt` containing a human-verified transcript, then run:

```powershell
python wer.py
```

WER is only meaningful when the reference transcript has been independently checked against the recording. The checked-in `outputs\wer_results.csv` is illustrative and uses a provisional reference; do not treat it as a final accuracy benchmark.

Generate speech from the Whisper transcript on Windows:

```powershell
.\tts.ps1
```

The generated transcripts, reference transcript, and TTS audio are stored under `outputs/` and included in this repository as example results.

## Notebook

Open `stutter_speech_pipeline.ipynb` in VS Code or Google Colab and run its cells. In Colab, upload the source audio when prompted, enter a human-verified reference transcript in the WER cell, and note that its gTTS cell requires an internet connection.

## Demonstration and report

- `report/mini_report.md` — project report and current evaluation caveats
- `report/asr_architecture.svg` — ASR and TTS architecture
- `report/three_minute_demo.md` — timed presentation narration

## Privacy and model limitations

This repository includes the source recording and speech-derived outputs; review the speaker's permissions before redistributing or reusing them. ASR output can omit, normalize, or alter disfluencies; WER from a single recording should not be generalized to broader model performance.

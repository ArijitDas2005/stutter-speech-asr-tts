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
- `stutter_speech_pipeline.ipynb` — complete, documented all-in-one project: setup, waveform/log-Mel analysis, Wav2Vec2/CTC, Whisper, WER, TTS, saved outputs, limitations, references, and a three-minute demo script. Designed for local Jupyter/VS Code and Google Colab.
- `report/` — mini-report, architecture diagram, and three-minute demo script
- `report/project_presentation.pptx` — 15-slide project presentation
- `report/full_project_report.pdf` — detailed 15-page project report
- `audio/stutter_current.mp3` — source audio used for the included example
- `outputs/` — waveform and spectrogram figures, ASR transcripts, provisional WER comparison, and synthesized TTS audio

**Audio privacy:** This public repository includes a voice recording, transcripts, and synthesized speech derived from it. Share or reuse these files only with the speaker's informed permission and any required rights. The recording is provided for this demonstration; do not assume it is cleared for unrelated reuse.

## Requirements

- Python 3.10 or later (the notebook can also run in Google Colab)
- Windows PowerShell for `tts.ps1`; the notebook TTS cell uses gTTS and needs internet access
- The included source audio file at `audio/stutter_current.mp3`. Replace that file to use another recording.

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

The refreshed ASR transcripts and plots are stored under `outputs/`. `wer_results.csv` currently compares the recognizers against a provisional Whisper-derived reference; regenerate WER after verifying the reference against the audio.

## All-in-one notebook

The complete runnable workflow and its documentation are consolidated in `stutter_speech_pipeline.ipynb`. Open it from the repository root in VS Code/Jupyter or upload it to Google Colab, install dependencies, and run the cells from top to bottom. In Colab, upload the source audio when prompted. The notebook saves the plots, ASR transcripts, WER comparison, architecture diagram, and synthesized audio under `outputs/`.

For a meaningful WER result, independently verify the reference transcript against the recording, enter it in the notebook, and mark it as verified. Otherwise, results based on the included provisional reference are explicitly labeled provisional. The notebook's gTTS cell requires internet access; it also includes an optional Windows System.Speech WAV cell.

The standalone scripts remain in the repository for command-line use; the notebook contains their functionality together in one portable document.

## Demonstration and report

- `report/mini_report.md` — project report and current evaluation caveats
- `report/full_project_report.pdf` — detailed 15-page report
- `report/project_presentation.pptx` — 15-slide widescreen presentation
- `report/generate_deliverables.py` — regenerates both deliverables from the current figures, transcripts, audio metadata, and WER results
- `report/asr_architecture.svg` — ASR and TTS architecture
- `report/three_minute_demo.md` — timed presentation narration

Regenerate the presentation and full report after updating outputs:

```powershell
python report\generate_deliverables.py
```

## Privacy and model limitations

This repository includes the source recording and speech-derived outputs; review the speaker's permissions before redistributing or reusing them. ASR output can omit, normalize, or alter disfluencies; WER from a single recording should not be generalized to broader model performance.

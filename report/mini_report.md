# From Voice to Text and Back
## ASR and TTS analysis of a speech sample with disfluencies

### Page 1 — Audio analysis, ASR, and CTC

#### Objective

The activity demonstrates an end-to-end speech technology pipeline on a short English recording containing observable disruptions to fluent speech. The goals are to inspect the audio, compare two automatic speech recognition (ASR) systems, explain Connectionist Temporal Classification (CTC), calculate word error rate (WER), and synthesize speech from recognized text. This is a technical demonstration only; it is not a clinical assessment of the speaker.

#### Input and signal analysis

The input is `audio/stutter_current.mp3`, a recording approximately 140.35 seconds long. Its decoded source rate is 48 kHz; the Wav2Vec2 pipeline resamples mono audio to 16 kHz. The waveform plots amplitude over time. The log-Mel spectrogram represents short-time spectral energy on a Mel-frequency scale, using 128 Mel bands, a 2048-sample FFT window, and a 512-sample hop. The plots show acoustic activity and pauses, but they do not independently identify or diagnose stuttering.

<table>
<tr>
<td><img src="../outputs/waveform.png" alt="Speech waveform" width="100%"></td>
<td><img src="../outputs/log_mel_spectrogram.png" alt="Log-Mel spectrogram" width="100%"></td>
</tr>
<tr><td align="center">Waveform</td><td align="center">Log-Mel spectrogram</td></tr>
</table>

#### ASR architectures and CTC

Two ASR paths are compared. Wav2Vec2 takes waveform samples, applies a convolutional feature encoder and Transformer context network, and emits character-level logits for CTC decoding. Whisper uses log-Mel audio features in an encoder-decoder Transformer and generates text tokens autoregressively. Whisper does not use CTC; the two approaches are parallel alternatives, not consecutive stages of one model.

CTC (Connectionist Temporal Classification) handles the unknown alignment between audio frames and output characters. Greedy decoding chooses the most likely token per frame, first merges consecutive repeated tokens, then removes blank tokens. For example, `A, A, blank, A, B, B` decodes to `AAB`. The blank separates the two A tokens, so removing blanks before merging repeats would give the wrong result. The example script [ctc_demo.py](../ctc_demo.py) shows this operation.

The full pipeline diagram is [ASR and TTS architecture](asr_architecture.svg).

\newpage

### Page 2 — Evaluation, TTS, and conclusion

#### ASR comparison and WER

The previous reference transcript describes the replaced recording and cannot be used for this sample. WER has not been calculated for the current audio. Add a human-verified verbatim transcript to `outputs/reference_transcript.txt`, then run `wer.py`.
#### Text-to-speech and conclusion

The `tts.ps1` script passes the Whisper transcript into Windows System.Speech and saves `outputs/tts_output.wav`. Synthesis for this new recording is still pending. The generated voice is synthetic; it is not the original speaker and does not reproduce the original disfluencies. The recording and speech-derived outputs are included in the repository; redistribution requires appropriate speaker permission.

The project now includes audio feature extraction and plots, two ASR implementations and outputs, a CTC decoding demonstration, a WER comparison script and table, a TTS generation script (new audio has not yet been synthesized), an ASR/TTS architecture diagram, this two-section mini-report, a runnable Jupyter/Colab notebook, and a timed presentation script. Run instructions and timing cues are in [three_minute_demo.md](three_minute_demo.md).

The major remaining scientific limitation is the lack of a verified ground-truth transcript. WER remains unavailable until the reference is verified against the new recording.

The expanded presentation and report are available as [project_presentation.pptx](project_presentation.pptx) and [full_project_report.pdf](full_project_report.pdf). These expanded files still reflect the previous run and must be regenerated after the reference and TTS output are refreshed.

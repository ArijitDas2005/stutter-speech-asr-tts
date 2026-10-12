import csv
from pathlib import Path
import re

from jiwer import process_words, wer


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"
REFERENCE_PATH = OUTPUT_DIR / "reference_transcript.txt"
HYPOTHESIS_PATHS = {
    "Wav2Vec2 CTC": OUTPUT_DIR / "asr_transcription.txt",
    "Whisper": OUTPUT_DIR / "whisper_transcription.txt",
}


def read_transcript(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Required transcript file was not found: {path}")

    text = path.read_text(encoding="utf-8").strip()
    if path.name == "asr_transcription.txt":
        lines = text.splitlines()
        if len(lines) >= 3 and lines[1].startswith("="):
            text = "\n".join(lines[2:]).strip()
    if not text:
        raise ValueError(f"Transcript file is empty: {path}")
    return text


def normalize_transcript(text: str) -> str:
    text = re.sub(r"[^\w\s']", " ", text.lower())
    return " ".join(text.split())


def main() -> None:
    reference = normalize_transcript(read_transcript(REFERENCE_PATH))
    rows = []

    print("=" * 78)
    print("WORD ERROR RATE (WER) MODEL COMPARISON")
    print("=" * 78)
    print("\nReference transcript (must be checked against the audio):")
    print(reference)

    for model_name, transcript_path in HYPOTHESIS_PATHS.items():
        hypothesis = normalize_transcript(read_transcript(transcript_path))
        result = process_words(reference, hypothesis)
        error_rate = wer(reference, hypothesis)
        rows.append(
            {
                "model": model_name,
                "reference_words": len(reference.split()),
                "hits": result.hits,
                "substitutions": result.substitutions,
                "deletions": result.deletions,
                "insertions": result.insertions,
                "wer": error_rate,
            }
        )

    print("\nModel comparison:")
    print(
        f"{'Model':<20} {'Hits':>6} {'Sub':>6} {'Del':>6} "
        f"{'Ins':>6} {'WER':>10}"
    )
    for row in rows:
        print(
            f"{row['model']:<20} {row['hits']:>6} "
            f"{row['substitutions']:>6} {row['deletions']:>6} "
            f"{row['insertions']:>6} {row['wer']:>9.2%}"
        )
        print(
            f"  WER = ({row['substitutions']} + {row['deletions']} + "
            f"{row['insertions']}) / {row['reference_words']}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results_path = OUTPUT_DIR / "wer_results.csv"
    with results_path.open("w", encoding="utf-8", newline="") as results_file:
        writer = csv.DictWriter(results_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDetailed results saved to: {results_path}")
    print(
        "Note: WER is only as reliable as the reference transcript. "
        "Verify it manually against the audio before reporting final accuracy."
    )


if __name__ == "__main__":
    main()

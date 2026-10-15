import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"
REPORT_DIR = PROJECT_DIR / "report"
PDF_PATH = REPORT_DIR / "mini_report.pdf"

NAVY = colors.HexColor("#16324F")
BLUE = colors.HexColor("#247BA0")
TEAL = colors.HexColor("#70C1B3")
PALE_BLUE = colors.HexColor("#EAF3F8")
PALE_TEAL = colors.HexColor("#E9F6F3")
INK = colors.HexColor("#23313F")
MUTED = colors.HexColor("#586878")
PALE_GOLD = colors.HexColor("#FFF4D6")


class PipelineDiagram(Flowable):
    def __init__(self, width, height=72):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        canvas = self.canv
        labels = [
            ("Speech", "MP3 input"),
            ("Features", "waveform + log-Mel"),
            ("ASR", "Wav2Vec2 / Whisper"),
            ("Text", "CTC / tokens + WER"),
            ("TTS", "synthesized WAV"),
        ]
        gap = 8
        box_width = (self.width - gap * (len(labels) - 1)) / len(labels)
        box_height = 48
        y = 13

        for index, (title, subtitle) in enumerate(labels):
            x = index * (box_width + gap)
            fill = PALE_BLUE if index % 2 == 0 else PALE_TEAL
            canvas.setFillColor(fill)
            canvas.setStrokeColor(BLUE if index % 2 == 0 else TEAL)
            canvas.roundRect(x, y, box_width, box_height, 7, fill=1, stroke=1)
            canvas.setFillColor(NAVY)
            canvas.setFont("Helvetica-Bold", 8.4)
            canvas.drawCentredString(x + box_width / 2, y + 29, title)
            canvas.setFillColor(MUTED)
            canvas.setFont("Helvetica", 6.4)
            canvas.drawCentredString(x + box_width / 2, y + 15, subtitle)

            if index < len(labels) - 1:
                arrow_start = x + box_width + 1
                arrow_end = arrow_start + gap - 2
                canvas.setStrokeColor(NAVY)
                canvas.setFillColor(NAVY)
                canvas.setLineWidth(1)
                canvas.line(arrow_start, y + box_height / 2, arrow_end, y + box_height / 2)
                canvas.line(arrow_end - 3, y + box_height / 2 + 3, arrow_end, y + box_height / 2)
                canvas.line(arrow_end - 3, y + box_height / 2 - 3, arrow_end, y + box_height / 2)


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=MUTED,
            spaceAfter=8,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=NAVY,
            spaceBefore=5,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "subsection": ParagraphStyle(
            "Subsection",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=BLUE,
            spaceBefore=4,
            spaceAfter=2,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.3,
            leading=11.2,
            textColor=INK,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=9.2,
            textColor=MUTED,
            spaceAfter=2,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=9,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceAfter=3,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.4,
            textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "TableHead",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.2,
            leading=8.5,
            textColor=colors.white,
            alignment=TA_LEFT,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=INK,
        ),
        "table_center": ParagraphStyle(
            "TableCenter",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=INK,
            alignment=TA_CENTER,
        ),
    }


def footer(canvas, doc):
    canvas.saveState()
    page_width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#D7E0E8"))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 14 * mm, page_width - doc.rightMargin, 14 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 9.5 * mm, "STUTTER SPEECH ASR & TTS | EDUCATIONAL DEMONSTRATION")
    canvas.drawRightString(page_width - doc.rightMargin, 9.5 * mm, f"{doc.page} / 2")
    canvas.restoreState()


def load_wer_rows():
    path = OUTPUT_DIR / "wer_results.csv"
    with path.open("r", encoding="utf-8", newline="") as result_file:
        return list(csv.DictReader(result_file))


def make_wer_table(rows, styles, available_width):
    headers = ["Model", "Decoding", "Hits", "Sub.", "Del.", "Ins.", "WER"]
    data = [[Paragraph(item, styles["table_head"]) for item in headers]]
    for row in rows:
        model = row["model"]
        decoding = "CTC greedy" if model.startswith("Wav2Vec2") else "Encoder-decoder"
        data.append(
            [
                Paragraph(model, styles["table_cell"]),
                Paragraph(decoding, styles["table_cell"]),
                Paragraph(row["hits"], styles["table_center"]),
                Paragraph(row["substitutions"], styles["table_center"]),
                Paragraph(row["deletions"], styles["table_center"]),
                Paragraph(row["insertions"], styles["table_center"]),
                Paragraph(f"{float(row['wer']):.2%}", styles["table_center"]),
            ]
        )

    widths = [
        available_width * 0.22,
        available_width * 0.25,
        available_width * 0.09,
        available_width * 0.09,
        available_width * 0.09,
        available_width * 0.09,
        available_width * 0.17,
    ]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_BLUE]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D7E0E8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def build_story(doc, styles):
    content_width = doc.width
    story = [
        Paragraph("From Voice to Text and Back", styles["title"]),
        Paragraph(
            "A two-page study of speech features, ASR, CTC, word error rate, and speech synthesis",
            styles["subtitle"],
        ),
        PipelineDiagram(content_width),
        Spacer(1, 2 * mm),
        Paragraph("1. Objective and audio analysis", styles["section"]),
        Paragraph(
            "This educational project demonstrates a complete speech technology pipeline using an English recording "
            "with speech disfluencies. It is a technical demonstration—not a clinical assessment or diagnostic tool. "
            "The source recording is approximately <b>140.35 seconds</b> at <b>48 kHz</b>; ASR input is mono audio "
            "resampled to <b>16 kHz</b> for Wav2Vec2.",
            styles["body"],
        ),
    ]

    figure_width = (content_width - 8 * mm) / 2
    figure_height = 47 * mm
    waveform = Image(str(OUTPUT_DIR / "waveform.png"), width=figure_width, height=figure_height)
    spectrogram = Image(
        str(OUTPUT_DIR / "log_mel_spectrogram.png"),
        width=figure_width,
        height=figure_height,
    )
    figure_table = Table(
        [
            [waveform, spectrogram],
            [
                Paragraph("Waveform: amplitude over time", styles["caption"]),
                Paragraph("Log-Mel spectrum: 128 bands; FFT 2048; hop 512", styles["caption"]),
            ],
        ],
        colWidths=[figure_width, figure_width],
        hAlign="LEFT",
    )
    figure_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    story.extend(
        [
            figure_table,
            Paragraph(
                "The log-Mel representation divides the waveform into overlapping short-time frames, maps spectral "
                "energy onto 128 Mel bands, and converts power to a decibel scale. Pauses or repeated acoustic "
                "patterns can be inspected in context, but visual features alone cannot establish a stutter or "
                "identify its cause.",
                styles["body"],
            ),
            Paragraph("2. ASR models and CTC decoding", styles["section"]),
            Paragraph(
                "<b>Wav2Vec2-base-960h</b> encodes waveform samples with a convolutional feature encoder and "
                "Transformer context network, then predicts character logits over time for CTC decoding. "
                "<b>Whisper-base</b> encodes log-Mel audio features and generates text tokens with an "
                "encoder-decoder Transformer. Whisper does not use CTC; these are alternative model paths.",
                styles["body"],
            ),
            Paragraph(
                "<b>Connectionist Temporal Classification (CTC)</b> handles unknown frame-to-character alignment. "
                "Greedy decoding first merges adjacent repeated tokens and then removes blank tokens. "
                "For example, A, A, blank, A, B, B becomes AAB: the blank preserves the second A.",
                styles["body"],
            ),
        ]
    )

    rows = load_wer_rows()
    story.extend(
        [
            PageBreak(),
            Paragraph("3. ASR comparison and word error rate", styles["section"]),
            Paragraph(
                "Both recognizers process the same recording, but use different model architectures and decoding "
                "strategies. The following results use the current 81-word reference transcript.",
                styles["body"],
            ),
        ]
    )
    story.append(make_wer_table(rows, styles, content_width))
    story.extend(
        [
            Spacer(1, 2 * mm),
            Paragraph(
                "<b>WER = (substitutions + deletions + insertions) / reference words.</b> "
                "With 81 reference words: Wav2Vec2 = (7 + 0 + 8) / 81 = <b>18.52%</b>; "
                "Whisper = (0 + 0 + 1) / 81 = <b>1.23%</b>.",
                styles["body"],
            ),
        ]
    )

    caution = Table(
        [
            [
                Paragraph(
                    "<b>Important evaluation limitation.</b> The 81-word reference has not been independently "
                    "verified and closely follows the Whisper transcript. This biases the comparison in Whisper's "
                    "favor. Treat these WER scores as provisional examples, not final accuracy claims. A human "
                    "transcript checked against the audio—including a consistent policy for disfluencies—is "
                    "needed for a valid comparison.",
                    styles["callout"],
                )
            ]
        ],
        colWidths=[content_width],
    )
    caution.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_GOLD),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#D6A94D")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.extend(
        [
            caution,
            Spacer(1, 2 * mm),
            Paragraph(
                "In this run, Wav2Vec2 has seven substitutions and eight insertions, while Whisper has one "
                "insertion and no substitutions or deletions against this reference. This describes only this "
                "recording and reference; it is not evidence of general model superiority.",
                styles["body"],
            ),
        ]
    )

    story.extend(
        [
            Paragraph("4. Text-to-speech and discussion", styles["section"]),
            Paragraph(
                "The Whisper transcript is passed to Windows System.Speech and synthesized as a WAV file. "
                "This completes the return path from recognized text to speech. The generated voice is synthetic: "
                "it is not the original speaker and does not preserve the original disfluencies.",
                styles["body"],
            ),
            Paragraph("5. Findings and limitations", styles["section"]),
            Paragraph(
                "The project produces waveform and log-Mel visualizations, two ASR transcripts, a CTC demonstration, "
                "a model comparison with substitution/deletion/insertion counts, and a TTS output. For this single "
                "recording, the provisional calculation favors Whisper. However, because the reference is not "
                "independent, that result cannot establish that Whisper is generally more accurate. Speech models "
                "may normalize, omit, or hallucinate disfluencies; WER also depends on transcription conventions, "
                "punctuation normalization, and the quality of the reference.",
                styles["body"],
            ),
            Paragraph("Reproducibility", styles["section"]),
            Paragraph(
                "The supplied scripts run audio visualization, Wav2Vec2 ASR, Whisper ASR, WER, and TTS as separate "
                "steps. The Jupyter/Colab notebook combines the workflow. The architecture diagram and timed demo "
                "script are provided in the report folder. Model downloads and notebook gTTS may require internet "
                "access; Windows System.Speech is used by the PowerShell TTS script.",
                styles["body"],
            ),
            Paragraph("Conclusion", styles["section"]),
            Paragraph(
                "This activity connects acoustic feature extraction to recognition and synthesis while contrasting "
                "CTC-based decoding with autoregressive token generation. The next essential research step is to "
                "prepare an independently verified verbatim transcript, rerun both recognizers under consistent "
                "normalization, and recalculate WER before making accuracy claims.",
                styles["body"],
            ),
            Spacer(1, 3 * mm),
        ]
    )

    details = [
        ["Input", "140.35-second English MP3, 48 kHz source; mono ASR"],
        ["Wav2Vec2", "facebook/wav2vec2-base-960h; CTC greedy decode"],
        ["Whisper", "base; CPU int8; English; beam size 5"],
        ["Features", "128 Mel bands; FFT 2048; hop 512"],
        ["TTS", "Windows System.Speech; synthetic output WAV"],
    ]
    details_table = Table(
        [
            [
                Paragraph(f"<b>{key}</b>", styles["table_cell"]),
                Paragraph(value, styles["table_cell"]),
            ]
            for key, value in details
        ],
        colWidths=[content_width * 0.22, content_width * 0.78],
    )
    details_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
                ("ROWBACKGROUNDS", (1, 0), (1, -1), [colors.white, PALE_BLUE]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D7E0E8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.extend(
        [
            details_table,
            Spacer(1, 3 * mm),
            Paragraph(
                "Privacy and interpretation: the recording and derived speech files require appropriate speaker "
                "permission before redistribution. This work demonstrates ASR/TTS behavior; it does not diagnose "
                "or assess a speech disorder.",
                styles["small"],
            ),
        ]
    )
    return story


def main():
    required_files = [
        OUTPUT_DIR / "waveform.png",
        OUTPUT_DIR / "log_mel_spectrogram.png",
        OUTPUT_DIR / "wer_results.csv",
    ]
    missing = [path for path in required_files if not path.is_file()]
    if missing:
        missing_list = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Cannot generate report; required files missing: {missing_list}")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=17 * mm,
        leftMargin=17 * mm,
        topMargin=15 * mm,
        bottomMargin=19 * mm,
        title="From Voice to Text and Back: ASR and TTS",
        author="Stutter Speech ASR and TTS Project",
        subject="Two-page analysis of speech feature extraction, ASR, CTC, WER, and TTS",
    )
    document.build(
        build_story(document, build_styles()),
        onFirstPage=footer,
        onLaterPages=footer,
    )
    print(f"Created two-page PDF: {PDF_PATH}")


if __name__ == "__main__":
    main()

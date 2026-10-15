$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$transcriptPath = Join-Path $projectRoot "outputs\whisper_transcription.txt"
$outputPath = Join-Path $projectRoot "outputs\tts_output.wav"

if (-not (Test-Path -LiteralPath $transcriptPath -PathType Leaf)) {
    throw "Whisper transcript not found: $transcriptPath"
}

$text = (Get-Content -LiteralPath $transcriptPath -Raw -Encoding UTF8).Trim()
if ([string]::IsNullOrWhiteSpace($text)) {
    throw "Whisper transcript is empty: $transcriptPath"
}

Add-Type -AssemblyName System.Speech
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $synthesizer.SetOutputToWaveFile($outputPath)
    $synthesizer.SpeakAsync($text)
    while ($synthesizer.State -ne [System.Speech.Synthesis.SynthesizerState]::Ready) {
        Start-Sleep -Milliseconds 100
    }
    $synthesizer.SetOutputToNull()
}
finally {
    $synthesizer.Dispose()
}

Write-Output "TTS speech saved to: $outputPath"

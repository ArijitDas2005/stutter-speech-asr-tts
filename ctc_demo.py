BLANK = 0
TOKEN_LABELS = {1: "A", 2: "B"}

# The blank between two A tokens allows both letters to survive decoding.
predicted_tokens = [BLANK, 1, 1, BLANK, 1, 2, 2, BLANK]

print("Greedy frame-level CTC tokens (0 is blank):")
print(predicted_tokens)

collapsed = []
previous = None
for token in predicted_tokens:
    if token != previous:
        collapsed.append(token)
    previous = token

print("\nAfter merging adjacent repeated tokens:")
print(collapsed)

decoded = [token for token in collapsed if token != BLANK]
transcription = "".join(TOKEN_LABELS[token] for token in decoded)

print("\nAfter removing blank tokens:")
print(decoded)
print(f"\nDecoded text: {transcription}")
print("A, blank, A remains AA; consecutive A, A collapses to A.")
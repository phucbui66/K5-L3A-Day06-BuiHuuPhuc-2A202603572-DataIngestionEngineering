
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "results"
OUTPUT.mkdir(parents=True, exist_ok=True)

scores = {
    "A": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "B": [1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    "C": [1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
}

reasons = {
    "A": [
        "Cut in middle of word",
        "Starts in middle of sentence",
        "Cuts start and end of explanation",
        "Ends in middle of sentence",
        "Incomplete exception example",
        "Cuts explanation at both ends",
        "Incomplete section context",
        "Starts and ends mid-explanation",
        "Cuts doctest explanation",
        "Fragment of previous sentence",
    ],
    "B": [
        "Complete introductory paragraph",
        "Complete explanation",
        "Complete explanation and examples",
        "Readable list operation examples",
        "Complete explanation",
        "Ends inside for-loop example",
        "Isolated sentence fragment",
        "Isolated sentence fragment",
        "Readable datetime examples",
        "Complete FAQ and footnote text",
    ],
}
reasons["C"] = reasons["B"]

path = OUTPUT / "coherence_scores.csv"

with path.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([
        "strategy", "position", "score", "reason"
    ])

    for strategy, values in scores.items():
        for position, score in enumerate(values, 1):
            writer.writerow([
                strategy,
                position,
                score,
                reasons[strategy][position - 1],
            ])

for strategy, values in scores.items():
    print(
        f"{strategy}: {sum(values)}/10 "
        f"({sum(values) * 10}%)"
    )

print("Saved:", path)
print("PASS: Coherence scores saved")

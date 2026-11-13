
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "results" / "coherence_review.md"

STRATEGIES = {
    "A": "chunks_fixed.jsonl",
    "B": "chunks_paragraph.jsonl",
    "C": "chunks_paragraph.jsonl",
}


def load_chunks(filename):
    path = INPUT / filename
    with path.open(encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def main():
    with OUTPUT.open("w", encoding="utf-8") as f:
        f.write("# Coherence Review\n\n")
        f.write(
            "Score: 1 = coherent, "
            "0 = fragmented or unclear.\n\n"
        )

        for strategy, filename in STRATEGIES.items():
            chunks = load_chunks(filename)

            # Deterministic positions across the collection
            indices = [
                round(i * (len(chunks) - 1) / 9)
                for i in range(10)
            ]

            f.write(f"## Strategy {strategy}\n\n")

            for number, index in enumerate(indices, 1):
                chunk = chunks[index]

                f.write(f"### Position {number}\n\n")
                f.write(f"Chunk index: {index}\n\n")
                f.write("```text\n")
                f.write(chunk["text"])
                f.write("\n```\n\n")
                f.write("Coherence score: TODO\n\n")
                f.write("---\n\n")

    print("Saved:", OUTPUT)
    print("PASS: Coherence samples exported")


if __name__ == "__main__":
    main()

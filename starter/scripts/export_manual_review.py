
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "results" / "retrieval_top3.jsonl"
OUTPUT = ROOT / "data" / "results" / "manual_review.md"

records = [
    json.loads(line)
    for line in INPUT.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

with OUTPUT.open("w", encoding="utf-8") as f:
    f.write("# Manual Retrieval Review\n\n")

    for strategy in ("A", "B", "C"):
        f.write(f"## Strategy {strategy}\n\n")

        selected = [
            r for r in records
            if r["strategy"] == strategy
            and r["split"] == "test"
        ]

        for record in selected:
            f.write(
                f"### {record['question_id']}: "
                f"{record['question']}\n\n"
            )

            f.write(
                f"**Expected answer:** "
                f"{record['answer']}\n\n"
            )

            f.write(
                f"**Gold evidence:**\n\n"
                f"> {record['gold_evidence']}\n\n"
            )

            f.write(
                f"**Required filter:** "
                f"`{record.get('filter')}`\n\n"
            )

            for chunk in record["top3"]:
                f.write(
                    f"#### Rank {chunk['rank']}\n\n"
                )
                f.write(
                    f"- Chunk: `{chunk['chunk_id']}`\n"
                    f"- Source: `{chunk['source']}`\n"
                    f"- Page: `{chunk['page']}`\n"
                    f"- Section: `{chunk['section']}`\n"
                    f"- Distance: `{chunk['distance']:.4f}`\n\n"
                )

                f.write("```text\n")
                f.write(chunk["text"])
                f.write("\n```\n\n")

            f.write("---\n\n")

print("Saved:", OUTPUT)
print("PASS: Manual review exported")

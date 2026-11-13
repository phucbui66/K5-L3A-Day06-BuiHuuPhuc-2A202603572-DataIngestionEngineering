
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "chunks_paragraph.jsonl"
OUTPUT = ROOT / "data" / "processed" / "source_overview.txt"

sections = defaultdict(list)

with INPUT.open("r", encoding="utf-8") as f:
    for line in f:
        chunk = json.loads(line)
        section = chunk["metadata"]["section"]
        sections[section].append(chunk)

with OUTPUT.open("w", encoding="utf-8") as f:
    for section, chunks in sorted(sections.items()):
        f.write(f"\n{'=' * 60}\n")
        f.write(f"SECTION: {section}\n")
        f.write(f"CHUNKS: {len(chunks)}\n")
        f.write(f"{'=' * 60}\n")

        for chunk in chunks[:5]:
            f.write(f"\nChunk ID: {chunk['chunk_id']}\n")
            f.write(f"Source: {chunk['source']}\n")
            f.write(f"Page: {chunk['page']}\n")
            f.write(f"Text:\n{chunk['text'][:500]}\n")
            f.write("-" * 40 + "\n")

print("Total sections:", len(sections))
print("Output:", OUTPUT)
print("PASS: Source overview generated")

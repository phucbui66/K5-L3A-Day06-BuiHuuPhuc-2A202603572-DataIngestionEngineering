
import json
import hashlib
import statistics
from collections import Counter
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "data" / "results"
DB_PATH = ROOT / "data" / "vector_store"

RESULTS.mkdir(parents=True, exist_ok=True)

STRATEGIES = {
    "A": {
        "file": "chunks_fixed.jsonl",
        "collection": "python_docs_fixed",
    },
    "B": {
        "file": "chunks_paragraph.jsonl",
        "collection": "python_docs_paragraph",
    },
    "C": {
        "file": "chunks_paragraph.jsonl",
        "collection": "python_docs_paragraph",
    },
}


def load_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def percentile(values, p):
    values = sorted(values)

    if not values:
        return 0

    index = (len(values) - 1) * p / 100
    low = int(index)
    high = min(low + 1, len(values) - 1)

    fraction = index - low

    return (
        values[low] * (1 - fraction)
        + values[high] * fraction
    )


def hash_file(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def main():
    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    report = {}

    for strategy, config in STRATEGIES.items():
        path = PROCESSED / config["file"]
        chunks = load_jsonl(path)

        lengths = [
            len(chunk["text"])
            for chunk in chunks
        ]

        ids = [
            chunk["chunk_id"]
            for chunk in chunks
        ]

        collection = client.get_collection(
            config["collection"]
        )

        unique_ids = len(set(ids))
        stored_count = collection.count()

        source_counts = Counter(
            chunk["source"]
            for chunk in chunks
        )

        stats = {
            "strategy": strategy,
            "chunk_count": len(chunks),
            "unique_chunk_ids": unique_ids,
            "duplicate_chunk_ids": len(ids) - unique_ids,
            "stored_vector_count": stored_count,
            "min_chars": min(lengths),
            "max_chars": max(lengths),
            "mean_chars": round(
                statistics.mean(lengths), 2
            ),
            "median_chars": round(
                statistics.median(lengths), 2
            ),
            "p90_chars": round(
                percentile(lengths, 90), 2
            ),
            "p95_chars": round(
                percentile(lengths, 95), 2
            ),
            "under_100_chars": sum(
                length < 100
                for length in lengths
            ),
            "over_500_chars": sum(
                length > 500
                for length in lengths
            ),
            "source_count": len(source_counts),
            "sha256": hash_file(path),
            "vector_count_matches": (
                stored_count == len(chunks)
            ),
        }

        report[strategy] = stats

        print(f"\n=== Strategy {strategy} ===")
        print("Chunks:", stats["chunk_count"])
        print("Unique IDs:", unique_ids)
        print("Stored vectors:", stored_count)
        print("Mean chars:", stats["mean_chars"])
        print("Median chars:", stats["median_chars"])
        print("P95 chars:", stats["p95_chars"])
        print("Max chars:", stats["max_chars"])
        print("Chunks >500:", stats["over_500_chars"])
        print(
            "Vector count matches:",
            stats["vector_count_matches"]
        )

        assert unique_ids == len(chunks), (
            f"Duplicate IDs in strategy {strategy}"
        )

        assert stored_count == len(chunks), (
            f"Vector count mismatch in {strategy}"
        )

        assert max(lengths) <= 500, (
            f"Chunk exceeds 500 chars in {strategy}"
        )

    output = RESULTS / "ingestion_statistics.json"

    output.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("\nSaved:", output)
    print("PASS: Ingestion statistics verified")


if __name__ == "__main__":
    main()

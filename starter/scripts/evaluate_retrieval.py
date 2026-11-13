
import csv
import json
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "results" / "retrieval_top3.jsonl"
OUTPUT = ROOT / "data" / "results"

# Proxy for evidence retrieval:
# At least 80 consecutive matching characters, or 50% of a
# shorter evidence span. This is NOT a manual grounding score.
MIN_MATCH_CHARS = 80
SHORT_EVIDENCE_RATIO = 0.5


def normalize(text):
    return " ".join((text or "").split()).casefold()


def evidence_match(gold_evidence, retrieved_text):
    gold = normalize(gold_evidence)
    found = normalize(retrieved_text)

    if not gold or not found:
        return False, 0

    match = SequenceMatcher(
        None, gold, found, autojunk=False
    ).find_longest_match(0, len(gold), 0, len(found))

    threshold = min(
        MIN_MATCH_CHARS,
        max(1, int(len(gold) * SHORT_EVIDENCE_RATIO)),
    )

    return match.size >= threshold, match.size


def evaluate(record):
    gold_units = {
        item["unit_id"]
        for item in record["gold_sources"]
    }

    top3 = record["top3"]

    # Source-unit Hit@1
    hit1 = bool(
        top3
        and top3[0].get("unit_id") in gold_units
    )

    # Evidence proxy: at least one retrieved chunk contains
    # a sufficiently long contiguous span of gold evidence.
    matches = [
        evidence_match(
            record["gold_evidence"],
            chunk.get("text", ""),
        )
        for chunk in top3
    ]

    evidence_hit3 = any(ok for ok, _ in matches)
    longest_match = max(
        (length for _, length in matches),
        default=0,
    )

    required_filter = record.get("filter")

    if required_filter:
        compliant = all(
            all(
                chunk.get(key) == value
                for key, value in required_filter.items()
            )
            for chunk in top3
        )
    else:
        compliant = None

    return {
        "question_id": record["question_id"],
        "split": record["split"],
        "strategy": record["strategy"],
        "hit_at_1": int(hit1),
        "evidence_hit_at_3_proxy": int(evidence_hit3),
        "longest_evidence_match_chars": longest_match,
        "filter_required": int(bool(required_filter)),
        "filter_compliant": (
            int(compliant)
            if compliant is not None
            else ""
        ),
        "top1_chunk_id": (
            top3[0]["chunk_id"] if top3 else ""
        ),
    }


def main():
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    records = [
        json.loads(line)
        for line in INPUT.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    assert len(records) == 60, (
        f"Expected 60 records, got {len(records)}"
    )

    rows = [evaluate(record) for record in records]

    seen = {
        (r["question_id"], r["strategy"])
        for r in rows
    }
    assert len(seen) == 60, "Duplicate retrieval results"

    detail_path = OUTPUT / "evaluation_detail.csv"

    with detail_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as f:
        writer = csv.DictWriter(
            f, fieldnames=list(rows[0].keys())
        )
        writer.writeheader()
        writer.writerows(rows)

    groups = defaultdict(list)

    for row in rows:
        groups[(row["split"], row["strategy"])].append(row)

    summary = []

    print("\n=== RETRIEVAL EVALUATION ===")

    for split in ("dev", "test"):
        print(f"\n{split.upper()}")

        for strategy in ("A", "B", "C"):
            group = groups[(split, strategy)]
            assert len(group) == (
                15 if split == "dev" else 5
            )

            total = len(group)

            hit1 = sum(r["hit_at_1"] for r in group)
            evidence = sum(
                r["evidence_hit_at_3_proxy"]
                for r in group
            )

            filtered = [
                r for r in group
                if r["filter_required"]
            ]

            compliance = (
                sum(r["filter_compliant"] for r in filtered)
                / len(filtered)
                if filtered else None
            )

            item = {
                "split": split,
                "strategy": strategy,
                "questions": total,
                "hit_at_1": round(hit1 / total, 4),
                "evidence_hit_at_3_proxy": round(
                    evidence / total, 4
                ),
                "filter_compliance": (
                    round(compliance, 4)
                    if compliance is not None
                    else None
                ),
            }

            summary.append(item)

            print(
                f"{strategy}: "
                f"Hit@1={item['hit_at_1']:.2%} | "
                f"Evidence@3(proxy)="
                f"{item['evidence_hit_at_3_proxy']:.2%} | "
                f"Filter compliance="
                f"{compliance:.2%}"
                if compliance is not None
                else (
                    f"{strategy}: "
                    f"Hit@1={item['hit_at_1']:.2%} | "
                    f"Evidence@3(proxy)="
                    f"{item['evidence_hit_at_3_proxy']:.2%}"
                )
            )

    summary_path = OUTPUT / "evaluation_summary.json"

    summary_path.write_text(
        json.dumps(
            summary, ensure_ascii=False, indent=2
        ) + "\n",
        encoding="utf-8",
    )

    print("\nSaved:", detail_path)
    print("Saved:", summary_path)
    print("PASS: Retrieval evaluation completed")


if __name__ == "__main__":
    main()

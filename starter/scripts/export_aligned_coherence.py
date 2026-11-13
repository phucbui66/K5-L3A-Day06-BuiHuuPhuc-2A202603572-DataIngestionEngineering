
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "data" / "results"

RESULTS.mkdir(parents=True, exist_ok=True)


def load_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def find_chunk(chunks, unit, position):
    unit_id = unit["unit_id"]
    document_id = unit["document_id"]

    candidates = []

    for chunk in chunks:
        meta = chunk.get("metadata", {})

        # Xác định đơn vị nguồn của chunk.
        chunk_unit_id = meta.get("unit_id")

        if chunk_unit_id is not None:
            if chunk_unit_id != unit_id:
                continue
        else:
            # Dự phòng: một số pipeline lưu unit_id
            # trong trường document_id.
            if chunk.get("document_id") != unit_id:
                continue

        # Offset tương đối trong source unit.
        start = meta.get("start_offset")
        end = meta.get("end_offset")

        # Nếu metadata lưu absolute offset,
        # quy đổi về offset của source unit.
        if start is None or end is None:
            abs_start = meta.get("absolute_start_offset")
            abs_end = meta.get("absolute_end_offset")

            unit_start = unit.get("start_offset")

            if unit_start is None:
                unit_start = meta.get("unit_start_offset")

            if (
                abs_start is not None
                and abs_end is not None
                and unit_start is not None
            ):
                start = abs_start - unit_start
                end = abs_end - unit_start

        if start is None or end is None:
            continue

        if start <= position < end:
            candidates.append(chunk)

    if not candidates:
        return None

    return min(
        candidates,
        key=lambda c: (
            c.get("metadata", {}).get(
                "end_offset", 10**12
            )
            - c.get("metadata", {}).get(
                "start_offset", 0
            )
        ),
    )


def main():
    units = load_jsonl(
        PROCESSED / "source_units.jsonl"
    )

    fixed = load_jsonl(
        PROCESSED / "chunks_fixed.jsonl"
    )

    paragraph = load_jsonl(
        PROCESSED / "chunks_paragraph.jsonl"
    )

    units = sorted(
        units,
        key=lambda u: u["unit_id"]
    )

    if len(units) < 10:
        raise ValueError(
            "Corpus must contain at least 10 source units"
        )

    # Chọn 10 vị trí nguồn trải đều trên corpus.
    indices = [
        round(i * (len(units) - 1) / 9)
        for i in range(10)
    ]

    output = RESULTS / "aligned_coherence_review.md"

    missing = []

    with output.open("w", encoding="utf-8") as f:
        f.write("# Aligned Coherence Review\n\n")

        f.write(
            "Scores: 0 = fragmented, "
            "1 = partially coherent, "
            "2 = fully coherent.\n\n"
        )

        f.write(
            "Sampling: 10 source units distributed "
            "across the sorted corpus; each position "
            "is the midpoint of its normalized text.\n\n"
        )

        for number, index in enumerate(indices, 1):
            unit = units[index]
            unit_id = unit["unit_id"]
            position = len(unit["text"]) // 2

            f.write(
                f"## Source Position {number}\n\n"
            )
            f.write(f"Unit: `{unit_id}`\n\n")
            f.write(f"Offset: `{position}`\n\n")

            for strategy, chunks in [
                ("A", fixed),
                ("B", paragraph),
                ("C", paragraph),
            ]:
                chunk = find_chunk(
                    chunks,
                    unit,
                    position
                )

                f.write(
                    f"### Strategy {strategy}\n\n"
                )

                if chunk is None:
                    missing.append(
                        (number, strategy, unit_id)
                    )
                    f.write("CHUNK NOT FOUND\n\n")
                    continue

                f.write(
                    f"Chunk ID: "
                    f"`{chunk['chunk_id']}`\n\n"
                )

                f.write("```text\n")
                f.write(chunk["text"])
                f.write("\n```\n\n")

                f.write("Score: TODO\n\n")
                f.write("Reason: TODO\n\n")

            f.write("---\n\n")

    print("Saved:", output)
    print("Source positions:", len(indices))
    print("Expected reviews:", len(indices) * 3)

    if missing:
        print("\nERROR: Missing chunks:")

        for number, strategy, unit_id in missing:
            print(
                f"Position {number}, "
                f"Strategy {strategy}, "
                f"Unit {unit_id}"
            )

        raise RuntimeError(
            f"Found {len(missing)} missing chunks. "
            "Check unit IDs and offset metadata."
        )

    print("PASS: All 30 chunks found")
    print("Ready for manual coherence scoring")


if __name__ == "__main__":
    main()

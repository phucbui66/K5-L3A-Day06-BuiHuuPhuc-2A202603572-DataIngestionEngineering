
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ingestion import load_txt

RAW_DIR = ROOT / "data" / "raw" / "tutorial"
OUTPUT = ROOT / "data" / "processed" / "source_units.jsonl"


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    count = 0

    with OUTPUT.open("w", encoding="utf-8") as f:
        for path in sorted(RAW_DIR.glob("*.txt")):
            units = load_txt(
                path=path,
                document_id=f"python_{path.stem}",
                source=path.name,
            )

            for unit in units:
                record = {
                    "unit_id": unit.metadata["unit_id"],
                    "document_id": unit.document_id,
                    "source": unit.source,
                    "page": unit.page,
                    "section": unit.metadata["section"],
                    "text": unit.text,
                    "char_count": len(unit.text),
                }

                f.write(
                    json.dumps(record, ensure_ascii=False)
                    + "\n"
                )

                count += 1

    print("Source units:", count)
    print("Output:", OUTPUT)

    assert count >= 30, "Not enough source units"

    print("PASS: Source units exported")


if __name__ == "__main__":
    main()

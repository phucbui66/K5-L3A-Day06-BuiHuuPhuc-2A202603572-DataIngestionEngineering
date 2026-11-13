
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ingestion import load_txt
from src.chunking import fixed_size, by_paragraph

RAW_DIR = ROOT / "data" / "raw" / "tutorial"
OUTPUT_DIR = ROOT / "data" / "processed"


def build_chunks():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fixed_path = OUTPUT_DIR / "chunks_fixed.jsonl"
    paragraph_path = OUTPUT_DIR / "chunks_paragraph.jsonl"

    fixed_count = 0
    paragraph_count = 0
    unit_count = 0

    fixed_ids = set()
    paragraph_ids = set()

    with (
        fixed_path.open("w", encoding="utf-8") as fixed_file,
        paragraph_path.open("w", encoding="utf-8") as paragraph_file,
    ):
        for path in sorted(RAW_DIR.glob("*.txt")):
            pages = load_txt(
                path=path,
                document_id=f"python_{path.stem}",
                source=path.name,
            )

            for page in pages:
                unit_count += 1

                fixed_chunks = fixed_size(
                    page,
                    size=500,
                    overlap=50,
                )

                paragraph_chunks = by_paragraph(
                    page,
                    max_size=500,
                )

                # Verify paragraph reconstruction
                assert (
                    "".join(c.text for c in paragraph_chunks)
                    == page.text
                )

                # ======================================
                # STRATEGY A: FIXED-SIZE CHUNKING
                # ======================================
                for chunk in fixed_chunks:
                    if chunk.chunk_id in fixed_ids:
                        raise ValueError(
                            f"Duplicate chunk ID: {chunk.chunk_id}"
                        )

                    fixed_ids.add(chunk.chunk_id)

                    # Preserve source unit metadata
                    unit_start = page.metadata["start_offset"]
                    unit_end = page.metadata["end_offset"]

                    chunk.metadata["unit_start_offset"] = unit_start
                    chunk.metadata["unit_end_offset"] = unit_end
                    chunk.metadata["unit_char_count"] = page.metadata[
                        "char_count"
                    ]

                    # Absolute offsets in normalized source
                    chunk.metadata["absolute_start_offset"] = (
                        unit_start + chunk.metadata["start_offset"]
                    )
                    chunk.metadata["absolute_end_offset"] = (
                        unit_start + chunk.metadata["end_offset"]
                    )

                    fixed_file.write(
                        json.dumps(
                            asdict(chunk),
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

                    fixed_count += 1

                # ======================================
                # STRATEGY B: PARAGRAPH-AWARE CHUNKING
                # ======================================
                for chunk in paragraph_chunks:
                    if chunk.chunk_id in paragraph_ids:
                        raise ValueError(
                            f"Duplicate chunk ID: {chunk.chunk_id}"
                        )

                    paragraph_ids.add(chunk.chunk_id)

                    # Preserve source unit metadata
                    unit_start = page.metadata["start_offset"]
                    unit_end = page.metadata["end_offset"]

                    chunk.metadata["unit_start_offset"] = unit_start
                    chunk.metadata["unit_end_offset"] = unit_end
                    chunk.metadata["unit_char_count"] = page.metadata[
                        "char_count"
                    ]

                    # Absolute offsets in normalized source
                    chunk.metadata["absolute_start_offset"] = (
                        unit_start + chunk.metadata["start_offset"]
                    )
                    chunk.metadata["absolute_end_offset"] = (
                        unit_start + chunk.metadata["end_offset"]
                    )

                    paragraph_file.write(
                        json.dumps(
                            asdict(chunk),
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

                    paragraph_count += 1

    print("========== CHUNK SUMMARY ==========")
    print("Source units:", unit_count)
    print("Fixed chunks:", fixed_count)
    print("Paragraph chunks:", paragraph_count)
    print("Fixed output:", fixed_path)
    print("Paragraph output:", paragraph_path)


if __name__ == "__main__":
    build_chunks()

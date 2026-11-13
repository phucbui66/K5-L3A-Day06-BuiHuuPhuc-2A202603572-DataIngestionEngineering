
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Đường dẫn gốc của thư mục starter
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ingestion import load_txt, normalize_text

DATA_DIR = ROOT / "data" / "raw" / "tutorial"
OUTPUT_FILE = ROOT / "data" / "manifest.json"

SOURCE_URL = "https://docs.python.org/3.15/"
DATASET_NAME = "Python Documentation - Tutorial"
VERSION = "3.15"


def calculate_sha256(path: Path) -> str:
    """Calculate SHA-256 hash of a source file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest() -> dict:
    """Build a traceable manifest for the Python tutorial corpus."""

    if not DATA_DIR.is_dir():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    files = sorted(DATA_DIR.glob("*.txt"))

    if not files:
        raise ValueError("No TXT files found in dataset directory")

    documents = []
    total_units = 0
    total_chars = 0
    skipped_files = []

    for path in files:
        document_id = f"python_{path.stem}"

        # Read and normalize source text
        raw_text = path.read_text(encoding="utf-8-sig")
        normalized = normalize_text(raw_text)

        # Load traceable source units
        pages = load_txt(
            path=path,
            document_id=document_id,
            source=path.name,
        )

        if not pages:
            skipped_files.append({
                "source": path.name,
                "reason": "No valid source unit (minimum 1500 characters)",
                "normalized_chars": len(normalized),
            })
            continue

        # Verify that splitting did not lose or duplicate content
        reconstructed = "".join(page.text for page in pages)
        if reconstructed != normalized:
            raise ValueError(f"Content mismatch in {path.name}")

        units = []

        for page in pages:
            meta = page.metadata

            if len(page.text) < 1500:
                raise ValueError(
                    f"Unit too short: {meta['unit_id']}"
                )

            units.append({
                "unit_id": meta["unit_id"],
                "page": page.page,
                "start_offset": meta["start_offset"],
                "end_offset": meta["end_offset"],
                "char_count": meta["char_count"],
            })

        documents.append({
            "document_id": document_id,
            "source": path.name,
            "source_path": path.relative_to(ROOT).as_posix(),
            "source_url": SOURCE_URL,
            "version": VERSION,
            "sha256": calculate_sha256(path),
            "normalized_char_count": len(normalized),
            "unit_count": len(units),
            "units": units,
        })

        total_units += len(units)
        total_chars += len(normalized)

        print(
            f"[OK] {path.name}: "
            f"{len(units)} units, {len(normalized)} chars"
        )

    return {
        "dataset": DATASET_NAME,
        "version": VERSION,
        "source_url": SOURCE_URL,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "minimum_unit_chars": 1500,
        "total_documents": len(documents),
        "total_units": total_units,
        "total_normalized_chars": total_chars,
        "skipped_files": skipped_files,
        "documents": documents,
    }


def main():
    manifest = build_manifest()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n========== DATASET SUMMARY ==========")
    print("Documents:", manifest["total_documents"])
    print("Valid units:", manifest["total_units"])
    print("Characters:", manifest["total_normalized_chars"])
    print("Skipped files:", len(manifest["skipped_files"]))
    print("Output:", OUTPUT_FILE)

    if manifest["total_units"] < 30:
        print("[WARNING] Corpus has fewer than 30 valid units")
    else:
        print("[PASS] Corpus has at least 30 valid units")


if __name__ == "__main__":
    main()

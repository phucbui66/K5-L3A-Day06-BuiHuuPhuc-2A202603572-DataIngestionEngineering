
import json
from pathlib import Path

from src.ingestion import (
    normalize_text,
    load_txt,
    split_into_units,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw" / "tutorial"
MANIFEST = ROOT / "data" / "manifest.json"


def test_normalize_preserves_indentation():
    text = "def hello():\r\n    print('Hi')\r\n\r\n\r\nDone"

    result = normalize_text(text)

    assert "    print('Hi')" in result
    assert "\r" not in result
    assert "\n\n\n" not in result


def test_split_preserves_content():
    text = "Python programming.\n\n" * 500

    units = split_into_units(text)

    assert len(units) > 1
    assert "".join(unit[0] for unit in units) == text
    assert all(len(unit[0]) >= 1500 for unit in units)


def test_unit_offsets():
    text = "Python documentation.\n\n" * 500

    units = split_into_units(text)

    previous_end = 0

    for unit_text, start, end in units:
        assert start == previous_end
        assert end > start
        assert text[start:end] == unit_text
        previous_end = end

    assert previous_end == len(text)


def test_load_txt_real_data():
    path = DATA_DIR / "controlflow.txt"

    pages = load_txt(
        path,
        document_id="python_controlflow",
        source="controlflow.txt",
    )

    assert len(pages) > 1

    unit_ids = [p.metadata["unit_id"] for p in pages]

    assert len(unit_ids) == len(set(unit_ids))
    assert all(len(p.text) >= 1500 for p in pages)
    assert all(p.source == "controlflow.txt" for p in pages)

    original = normalize_text(path.read_text(encoding="utf-8-sig"))

    assert "".join(p.text for p in pages) == original


def test_manifest_integrity():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["total_units"] >= 30
    assert manifest["total_documents"] >= 1

    counted_units = sum(
        doc["unit_count"]
        for doc in manifest["documents"]
    )

    assert counted_units == manifest["total_units"]

    for doc in manifest["documents"]:
        assert len(doc["units"]) == doc["unit_count"]

        for unit in doc["units"]:
            assert unit["char_count"] >= 1500
            assert (
                unit["end_offset"] - unit["start_offset"]
                == unit["char_count"]
            )

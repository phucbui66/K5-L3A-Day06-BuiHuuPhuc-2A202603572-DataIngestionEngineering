
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifest.json"

data = json.loads(MANIFEST.read_text(encoding="utf-8"))

required = [
    "document_id",
    "source_path",
    "source_url",
    "version",
    "sha256",
    "license_or_permission",
    "accessed_at",
]

print("=== MANIFEST METADATA CHECK ===")

for field in required:
    missing = [
        doc.get("document_id", "unknown")
        for doc in data["documents"]
        if not doc.get(field)
    ]
    print(
        f"{field}: "
        f"{'PASS' if not missing else 'MISSING'} "
        f"({len(missing)} documents)"
    )

invalid_units = []

for doc in data["documents"]:
    for unit in doc["units"]:
        if unit["char_count"] < 1500:
            invalid_units.append(unit["unit_id"])

print("Total documents:", len(data["documents"]))
print("Total units:", data["total_units"])
print("Units below 1500 chars:", len(invalid_units))

if invalid_units:
    print("Invalid units:", invalid_units)

print("PASS: Manifest inspection completed")

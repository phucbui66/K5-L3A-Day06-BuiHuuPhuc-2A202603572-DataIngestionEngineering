
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "manifest.json"

LICENSE = "Python Software Foundation License Version 2 (PSF-2.0)"
LICENSE_URL = "https://docs.python.org/3.15/license.html"

data = json.loads(PATH.read_text(encoding="utf-8"))

# Chỉ sử dụng ngày truy cập gốc khi có bằng chứng.
# Không lấy ngày tạo manifest làm ngày truy cập nguồn.
accessed_at = data.get("accessed_at")

if not accessed_at:
    accessed_at = input(
        "Nhap ngay truy cap nguon thuc te "
        "(ISO 8601, vd 2026-11-13T19:00:00+00:00), "
        "hoac Enter neu khong biet: "
    ).strip()

if accessed_at:
    try:
        parsed = datetime.fromisoformat(
            accessed_at.replace("Z", "+00:00")
        )
        if parsed.tzinfo is None:
            raise ValueError("Timezone is required")
    except ValueError as exc:
        raise SystemExit(f"Invalid accessed_at: {exc}")
else:
    accessed_at = None

data["license_or_permission"] = LICENSE
data["license_url"] = LICENSE_URL

if accessed_at:
    data["accessed_at"] = accessed_at

for doc in data["documents"]:
    doc["license_or_permission"] = LICENSE
    doc["license_url"] = LICENSE_URL

    doc_accessed = doc.get("accessed_at") or accessed_at
    if doc_accessed:
        doc["accessed_at"] = doc_accessed

PATH.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)

print("Documents updated:", len(data["documents"]))
print("License:", LICENSE)
print("Accessed at:", accessed_at or "UNKNOWN")
print("Saved:", PATH)

"""Read and normalize source data. TODO: implement functions."""
import re
import unicodedata
from pathlib import Path
from .models import DocumentPage


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    """TODO: extract each physical page; keep its page number and source.

    Detect and record pages with no text. OCR, when needed, is a separate step.
    """
    raise NotImplementedError("TODO: load_pdf")


def normalize_text(text: str) -> str:
    """Normalize text while preserving Python code indentation."""

    # 1. Chuẩn hóa Unicode
    text = unicodedata.normalize("NFC", text)

    # 2. Chuẩn hóa xuống dòng
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 3. Thay tab bằng 4 dấu cách
    text = text.expandtabs(4)

    # 4. Xóa khoảng trắng ở cuối từng dòng
    lines = [
        line.rstrip()
        for line in text.split("\n")
    ]

    # 5. Ghép các dòng lại
    text = "\n".join(lines)

    # 6. Giảm các dòng trống liên tiếp
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 7. Xóa dòng trống ở đầu và cuối tài liệu
    return text.strip("\n")
def load_txt(
    path: Path,
    document_id: str,
    source: str,
) -> list[DocumentPage]:
    """Read a TXT file and preserve source traceability."""

    # 1. Kiểm tra file có tồn tại không
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    # 2. Đọc nội dung UTF-8
    raw_text = path.read_text(encoding="utf-8-sig")

    # 3. Chuẩn hóa nội dung
    text = normalize_text(raw_text)

    # 4. Kiểm tra file rỗng
    if not text:
        return []

    # 5. Chia văn bản thành các đơn vị nguồn
    units = split_into_units(text)

    # 6. Tạo DocumentPage cho từng đơn vị
    pages = []

    for index, (unit_text, start, end) in enumerate(units, start=1):
        unit_id = f"{document_id}_unit_{index:03d}"

        page = DocumentPage(
            document_id=document_id,
            source=source,
            page=index,
            text=unit_text,
            metadata={
                "file_type": "txt",
                "section": path.stem,
                "version": "3.15",
                "unit_id": unit_id,
                "start_offset": start,
                "end_offset": end,
                "char_count": len(unit_text),
            },
        )

        pages.append(page)

    return pages
def split_into_units(
    text: str,
    min_chars: int = 1500,
    target_chars: int = 3000,
) -> list[tuple[str, int, int]]:
    """
    Split normalized text into sequential source units.

    Returns:
        List of (unit_text, start_offset, end_offset).
        Offsets refer to the normalized text.
    """
    if min_chars <= 0 or target_chars < min_chars:
        raise ValueError("Invalid unit size")

    if not text:
        return []

    if len(text) < min_chars:
        return []

    units = []
    start = 0
    total = len(text)

    while start < total:
        remaining = total - start

        # Gộp phần cuối nếu không đủ min_chars
        if remaining < min_chars:
            previous_text, previous_start, _ = units[-1]
            units[-1] = (
                text[previous_start:total],
                previous_start,
                total,
            )
            break

        # Chọn điểm kết thúc dự kiến
        end = min(start + target_chars, total)

        # Nếu phần cuối quá ngắn, gộp luôn vào unit này
        if 0 < total - end < min_chars:
            end = total

        # Ưu tiên ngắt tại dòng trống hoặc xuống dòng
        if end < total:
            paragraph_end = text.rfind(
                "\n\n", start + min_chars, end
            )

            if paragraph_end != -1:
                end = paragraph_end + 2
            else:
                line_end = text.rfind(
                    "\n", start + min_chars, end
                )
                if line_end != -1:
                    end = line_end + 1

        # Bảo đảm không tạo unit quá ngắn
        if end - start < min_chars:
            end = min(start + target_chars, total)

        units.append((text[start:end], start, end))
        start = end

    return units

"""Implement fixed-size and structure-aware chunking."""

from .models import Chunk, DocumentPage


def fixed_size(
    page: DocumentPage,
    size: int,
    overlap: int,
) -> list[Chunk]:
    """Split text into overlapping windows and retain source metadata."""

    # 1. Validate parameters
    if size <= 0:
        raise ValueError("size must be greater than 0")

    if overlap < 0 or overlap >= size:
        raise ValueError("overlap must satisfy 0 <= overlap < size")

    text = page.text

    if not text:
        return []

    # 2. Calculate sliding-window step
    step = size - overlap
    chunks = []

    # 3. Create overlapping chunks
    for index, start in enumerate(range(0, len(text), step), start=1):
        end = min(start + size, len(text))

        # Avoid creating a redundant trailing chunk
        if chunks and end == len(text) and start < chunks[-1].metadata["end_offset"]:
            if end <= chunks[-1].metadata["end_offset"]:
                break

        chunk_text = text[start:end]

        chunk_id = (
            f"{page.document_id}_"
            f"p{page.page:03d}_"
            f"fixed_{index:03d}"
        )

        metadata = {
            **page.metadata,
            "strategy": "fixed",
            "chunk_index": index,
            "start_offset": start,
            "end_offset": end,
            "char_count": len(chunk_text),
            "chunk_size": size,
            "overlap": overlap,
        }

        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=chunk_text,
                metadata=metadata,
            )
        )

        if end == len(text):
            break

    return chunks



def by_paragraph(page: DocumentPage, max_size: int) -> list[Chunk]:
    """Group paragraphs and split oversized paragraphs with traceability."""

    if max_size <= 0:
        raise ValueError("max_size must be greater than 0")

    text = page.text

    if not text:
        return []

    # 1. Identify paragraph boundaries while retaining separators
    paragraphs = []
    start = 0

    while start < len(text):
        boundary = text.find("\n\n", start)

        if boundary == -1:
            paragraphs.append((start, len(text)))
            break

        end = boundary + 2
        paragraphs.append((start, end))
        start = end

    # 2. Build chunk ranges
    ranges = []
    current_start = None
    current_end = None

    def flush():
        nonlocal current_start, current_end

        if current_start is not None and current_end > current_start:
            ranges.append((current_start, current_end))

        current_start = None
        current_end = None

    for para_start, para_end in paragraphs:
        para_length = para_end - para_start

        # Oversized paragraph: split into smaller ranges
        if para_length > max_size:
            flush()
            pos = para_start

            while pos < para_end:
                limit = min(pos + max_size, para_end)
                end = limit

                # Prefer newline boundaries
                if limit < para_end:
                    newline = text.rfind("\n", pos + 1, limit)

                    if newline != -1:
                        end = newline + 1

                # Avoid an empty range
                if end <= pos:
                    end = limit

                ranges.append((pos, end))
                pos = end

            continue

        # Start a new chunk
        if current_start is None:
            current_start = para_start
            current_end = para_end

        # Add paragraph if it fits
        elif para_end - current_start <= max_size:
            current_end = para_end

        # Otherwise finish current chunk
        else:
            flush()
            current_start = para_start
            current_end = para_end

    flush()

    # 3. Create Chunk objects
    chunks = []

    for index, (start, end) in enumerate(ranges, start=1):
        chunk_text = text[start:end]

        chunk_id = (
            f"{page.document_id}_"
            f"p{page.page:03d}_"
            f"paragraph_{index:03d}"
        )

        metadata = {
            **page.metadata,
            "strategy": "paragraph",
            "chunk_index": index,
            "start_offset": start,
            "end_offset": end,
            "char_count": len(chunk_text),
            "max_size": max_size,
            "overlap": 0,
        }

        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=chunk_text,
                metadata=metadata,
            )
        )

    return chunks


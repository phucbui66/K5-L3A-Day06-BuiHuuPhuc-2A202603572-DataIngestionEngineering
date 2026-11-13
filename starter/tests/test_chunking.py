
import pytest

from src.models import DocumentPage
from src.chunking import fixed_size, by_paragraph


def make_page(text):
    return DocumentPage(
        document_id="test_doc",
        source="test.txt",
        page=1,
        text=text,
        metadata={"unit_id": "test_doc_unit_001"},
    )


def test_fixed_size_windows():
    page = make_page("A" * 1200)

    chunks = fixed_size(page, size=500, overlap=50)

    assert len(chunks) == 3

    assert len(chunks[0].text) == 500
    assert len(chunks[1].text) == 500
    assert len(chunks[2].text) == 300

    assert chunks[0].metadata["start_offset"] == 0
    assert chunks[1].metadata["start_offset"] == 450
    assert chunks[2].metadata["start_offset"] == 900


def test_fixed_size_overlap():
    page = make_page("".join(str(i % 10) for i in range(1200)))

    chunks = fixed_size(page, size=500, overlap=50)

    for i in range(len(chunks) - 1):
        assert chunks[i].text[-50:] == chunks[i + 1].text[:50]


def test_fixed_size_traceability():
    page = make_page("Python " * 200)

    chunks = fixed_size(page, size=500, overlap=50)

    for chunk in chunks:
        assert chunk.document_id == page.document_id
        assert chunk.source == page.source
        assert chunk.page == page.page
        assert chunk.metadata["unit_id"] == "test_doc_unit_001"


def test_fixed_size_invalid_parameters():
    page = make_page("Hello world")

    with pytest.raises(ValueError):
        fixed_size(page, size=0, overlap=0)

    with pytest.raises(ValueError):
        fixed_size(page, size=500, overlap=500)

    with pytest.raises(ValueError):
        fixed_size(page, size=500, overlap=-1)


def test_fixed_size_empty_text():
    page = make_page("")

    assert fixed_size(page, size=500, overlap=50) == []

def test_paragraph_grouping():
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

    page = make_page(text)
    chunks = by_paragraph(page, max_size=40)

    assert len(chunks) >= 2
    assert "".join(c.text for c in chunks) == text
    assert all(len(c.text) <= 40 for c in chunks)


def test_paragraph_oversized():
    text = "A" * 1200

    page = make_page(text)
    chunks = by_paragraph(page, max_size=500)

    assert len(chunks) == 3
    assert [len(c.text) for c in chunks] == [500, 500, 200]
    assert "".join(c.text for c in chunks) == text


def test_paragraph_offsets():
    text = ("Python documentation.\n\n" * 100)

    page = make_page(text)
    chunks = by_paragraph(page, max_size=500)

    previous_end = 0

    for chunk in chunks:
        start = chunk.metadata["start_offset"]
        end = chunk.metadata["end_offset"]

        assert start == previous_end
        assert text[start:end] == chunk.text
        assert len(chunk.text) <= 500

        previous_end = end

    assert previous_end == len(text)


def test_paragraph_traceability():
    page = make_page("Python\n\nDocumentation\n\n" * 30)

    chunks = by_paragraph(page, max_size=500)

    ids = [c.chunk_id for c in chunks]

    assert len(ids) == len(set(ids))

    for chunk in chunks:
        assert chunk.document_id == page.document_id
        assert chunk.source == page.source
        assert chunk.page == page.page
        assert chunk.metadata["unit_id"] == "test_doc_unit_001"
        assert chunk.metadata["strategy"] == "paragraph"


def test_paragraph_invalid_and_empty():
    page = make_page("Hello world")

    with pytest.raises(ValueError):
        by_paragraph(page, max_size=0)

    assert by_paragraph(make_page(""), max_size=500) == []

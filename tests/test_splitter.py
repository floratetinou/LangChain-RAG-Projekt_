
from langchain_core.documents import Document

from src.local_rag.splitter import split_documents


def test_split_documents_creates_multiple_chunks():
    """Prüft, ob ein langer Text in mehrere Chunks aufgeteilt wird."""

    document = Document(
        page_content=(
            "DoIP bedeutet Diagnostics over Internet Protocol. "
            "Es ermöglicht die Fahrzeugdiagnose über IP-Netzwerke. "
            "Die Kommunikation nutzt Ethernet. "
        ) * 10,
        metadata={"source": "test_document.txt", "file_type": "txt"},
    )

    chunks = split_documents(
        [document],
        chunk_size=100,
        chunk_overlap=10,
    )

    assert len(chunks) > 1
    assert all(chunk.page_content.strip() for chunk in chunks)
    assert all(
        chunk.metadata["source"] == "test_document.txt"
        for chunk in chunks
    )


def test_markdown_headers_are_saved_as_metadata():
    """Prüft, ob Markdown-Überschriften als Metadaten gespeichert werden."""

    document = Document(
        page_content=(
            "# DoIP\n"
            "DoIP bedeutet Diagnostics over Internet Protocol.\n\n"
            "## Vorteile\n"
            "DoIP ermöglicht eine Diagnose über Ethernet.\n"
        ),
        metadata={"source": "test.md", "file_type": "md"},
    )

    chunks = split_documents(
        [document],
        chunk_size=500,
        chunk_overlap=50,
    )

    assert len(chunks) >= 2
    assert any(
        chunk.metadata.get("header_1") == "DoIP"
        for chunk in chunks
    )
    assert any(
        chunk.metadata.get("header_2") == "Vorteile"
        for chunk in chunks
    )
    assert all(chunk.metadata["source"] == "test.md" for chunk in chunks)


def test_empty_document_list_returns_no_chunks():
    """Prüft, ob eine leere Dokumentliste korrekt behandelt wird."""

    chunks = split_documents(
        [],
        chunk_size=250,
        chunk_overlap=40,
    )

    assert chunks == []

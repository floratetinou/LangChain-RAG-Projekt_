
from pathlib import Path

import pytest
from langchain_core.documents import Document

import src.local_rag.loaders as loaders


def test_load_file_txt_adds_common_metadata(tmp_path):
    """Prüft das Laden einer Textdatei und die gemeinsamen Metadaten."""

    file_path = tmp_path / "doip.txt"
    file_path.write_text(
        "DoIP bedeutet Diagnostics over Internet Protocol.",
        encoding="utf-8",
    )

    documents = loaders.load_file(file_path)

    assert len(documents) == 1
    assert "DoIP" in documents[0].page_content
    assert documents[0].metadata["file_name"] == "doip.txt"
    assert documents[0].metadata["file_type"] == "txt"
    assert documents[0].metadata["source"] == str(file_path.resolve())


def test_load_file_markdown(tmp_path):
    """Prüft, ob eine Markdown-Datei korrekt geladen wird."""

    file_path = tmp_path / "wissen.md"
    file_path.write_text(
        "# DoIP\n\nDiagnose über Ethernet.",
        encoding="utf-8",
    )

    documents = loaders.load_file(file_path)

    assert len(documents) == 1
    assert "# DoIP" in documents[0].page_content
    assert documents[0].metadata["file_type"] == "md"


def test_load_file_rejects_unsupported_format(tmp_path):
    """Prüft, ob nicht unterstützte Dateiformate abgelehnt werden."""

    file_path = tmp_path / "daten.csv"
    file_path.write_text("a,b\n1,2", encoding="utf-8")

    with pytest.raises(ValueError, match="Nicht unterst"):
        loaders.load_file(file_path)


def test_load_directory_finds_supported_files(tmp_path):
    """Prüft, ob unterstützte Dateien auch in Unterordnern gefunden werden."""

    (tmp_path / "doip.txt").write_text(
        "DoIP Text",
        encoding="utf-8",
    )

    subdirectory = tmp_path / "docs"
    subdirectory.mkdir()

    (subdirectory / "wissen.md").write_text(
        "# Wissen\n\nMarkdown-Inhalt.",
        encoding="utf-8",
    )

    (tmp_path / "daten.csv").write_text(
        "a,b\n1,2",
        encoding="utf-8",
    )

    documents = loaders.load_directory(tmp_path)

    assert len(documents) == 2
    assert {doc.metadata["file_type"] for doc in documents} == {"txt", "md"}
    assert {doc.metadata["file_name"] for doc in documents} == {
        "doip.txt",
        "wissen.md",
    }

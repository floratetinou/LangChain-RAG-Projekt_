from pathlib import Path
from src.local_rag.loaders import load_file

def test_markdown_loader_keeps_basic_metadata():
    path = Path("data/beispiel_wissensbasis.md")
    docs = load_file(path)
    assert docs
    assert docs[0].metadata["file_name"] == path.name
    assert docs[0].metadata["file_type"] == "md"
    assert "Fahrzeugdiagnose" in docs[0].page_content

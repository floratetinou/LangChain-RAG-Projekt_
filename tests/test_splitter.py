from pathlib import Path
from src.local_rag.loaders import load_file
from src.local_rag.splitter import split_documents

def test_markdown_is_split_and_headers_are_preserved():
    docs = load_file(Path("data/beispiel_wissensbasis.md"))
    chunks = split_documents(docs, chunk_size=250, chunk_overlap=40)
    assert len(chunks) > 1
    assert all(chunk.metadata.get("file_type") == "md" for chunk in chunks)
    assert any(chunk.metadata.get("header_2") == "DoIP" for chunk in chunks)

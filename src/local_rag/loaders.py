from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader

SUPPORTED_SUFFIXES = {".pdf", ".txt", ".md"}

def _add_common_metadata(doc: Document, path: Path) -> Document:
    doc.metadata.update({
        "source": str(path.resolve()),
        "file_name": path.name,
        "file_type": path.suffix.lower().lstrip("."),
    })
    return doc

def load_file(path: Path) -> list[Document]:
    """Lädt PDF, TXT oder Markdown. PyMuPDFLoader erhält PDF-Seitenmetadaten."""
    path = Path(path)
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Nicht unterstützter Dateityp: {path.suffix}")
    if path.suffix.lower() == ".pdf":
        docs = PyMuPDFLoader(str(path)).load()
    else:
        docs = TextLoader(str(path), encoding="utf-8", autodetect_encoding=True).load()
    return [_add_common_metadata(doc, path) for doc in docs]

def load_directory(directory: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(Path(directory).rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            documents.extend(load_file(path))
    return documents

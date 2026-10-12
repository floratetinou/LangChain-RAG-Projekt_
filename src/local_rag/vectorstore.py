
import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from .config import Settings

logger = logging.getLogger(__name__)


def create_embeddings(cfg: Settings) -> OllamaEmbeddings:
    """Erstellt das lokale Ollama-Embedding-Modell."""
    return OllamaEmbeddings(
        model=cfg.embedding_model,
        base_url=cfg.ollama_base_url,
    )


def open_vectorstore(cfg: Settings) -> Chroma:
    """Öffnet den persistenten ChromaDB-Vektorindex."""
    cfg.chroma_dir.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=cfg.collection_name,
        embedding_function=create_embeddings(cfg),
        persist_directory=str(cfg.chroma_dir),
    )


def index_documents(
    vectorstore: Chroma,
    documents: list[Document],
) -> int:
    """Fügt Dokument-Chunks zum Vektorindex hinzu."""
    if not documents:
        logger.warning("Keine Dokumente zur Indexierung vorhanden.")
        return 0

    logger.info("Indexierung von %s Chunks gestartet.", len(documents))

    vectorstore.add_documents(documents)

    logger.info("Indexierung abgeschlossen.")
    return len(documents)


def rebuild_index(
    vectorstore: Chroma,
    documents: list[Document],
) -> int:
    """Ersetzt den bisherigen Index durch neue Dokument-Chunks."""

    if not documents:
        raise ValueError(
            "Der Index kann nicht mit einer leeren Dokumentliste "
            "neu aufgebaut werden."
        )

    logger.warning("Der bestehende Vektorindex wird zurückgesetzt.")

    # Alte Einträge entfernen und die Collection neu erstellen.
    vectorstore.reset_collection()

    # Neue Chunks indexieren.
    vectorstore.add_documents(documents)

    logger.info(
        "Index erfolgreich neu aufgebaut: %s Chunks.",
        len(documents),
    )

    return len(documents)

import logging

from src.local_rag.config import settings
from src.local_rag.ui import build_ui
from src.local_rag.vectorstore import open_vectorstore


def configure_logging() -> None:
    """Konfiguriert das Logging für die Anwendung."""
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    """Startet die lokale RAG-Anwendung."""
    configure_logging()

    logger = logging.getLogger(__name__)
    logger.info("Starte die lokale RAG-Anwendung.")

    try:
        store = open_vectorstore(settings)
        logger.info("ChromaDB-Vektorindex wurde geöffnet.")

        ui = build_ui(store, settings)

        logger.info(
            "Starte Gradio auf http://%s:%s",
            settings.gradio_host,
            settings.gradio_port,
        )

        ui.launch(
            server_name=settings.gradio_host,
            server_port=settings.gradio_port,
        )

    except Exception:
        logger.exception(
            "Die RAG-Anwendung konnte nicht gestartet werden."
        )
        raise


if __name__ == "__main__":
    main()

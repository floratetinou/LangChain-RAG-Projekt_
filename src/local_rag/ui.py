
import logging
from pathlib import Path

import gradio as gr

from .config import Settings
from .loaders import load_file
from .pipeline import answer_question_with_details
from .splitter import split_documents
from .vectorstore import rebuild_index

logger = logging.getLogger(__name__)


def build_ui(vectorstore, cfg: Settings) -> gr.Blocks:
    """Erstellt die Gradio-Oberfläche für die lokale RAG-Anwendung."""

    def upload_pdf(file_path: str | None) -> str:
        """Lädt ein PDF und erstellt einen neuen Vektorindex."""
        if not file_path:
            return "Bitte zuerst eine PDF-Datei auswählen."

        try:
            path = Path(file_path)

            if path.suffix.lower() != ".pdf":
                return "Fehler: Bitte eine PDF-Datei hochladen."

            # PDF laden.
            documents = load_file(path)

            if not documents:
                return "Das PDF enthält keine lesbaren Seiten."

            # Dokumente in Chunks aufteilen.
            chunks = split_documents(
                documents,
                cfg.chunk_size,
                cfg.chunk_overlap,
            )

            if not chunks:
                return "Das PDF enthält keinen indexierbaren Text."

            # Bestehenden Index durch das neue PDF ersetzen.
            count = rebuild_index(vectorstore, chunks)

            logger.info(
                "PDF '%s' erfolgreich indexiert: %s Chunks.",
                path.name,
                count,
            )

            return (
                f"PDF erfolgreich indexiert: {path.name}\n\n"
                f"Seiten: {len(documents)}\n"
                f"Chunks: {count}"
            )

        except Exception:
            logger.exception("Fehler beim PDF-Upload.")

            return (
                "Das PDF konnte nicht verarbeitet werden. "
                "Bitte die Fehlermeldung im Terminal prüfen."
            )

    def ask(question: str, mode: str) -> tuple[str, str]:
        """Beantwortet eine Frage und zeigt Retrieval-Details an."""
        if not question or not question.strip():
            return "Bitte eine Frage eingeben.", ""

        try:
            answer, sources, details = answer_question_with_details(
                question,
                mode,
                vectorstore,
                cfg,
            )

            # Quellen vorbereiten.
            source_block = "\n".join(
                f"- {source}" for source in sources
            ) or "- Keine"

            # Gefundene Chunks und Scores vorbereiten.
            chunks_block = []

            for i, item in enumerate(details, start=1):
                score = item.get("score")

                if score is None:
                    score_text = "Nicht verfügbar"
                else:
                    score_text = f"{score:.4f}"

                chunks_block.append(
                    f"### Chunk {i}\n\n"
                    f"**Quelle:** {item['source']}\n\n"
                    f"**Relevanzscore:** {score_text}\n\n"
                    f"**Text:**\n\n{item['content']}"
                )

            details_markdown = (
                f"## Quellen\n\n{source_block}\n\n"
                "## Gefundene Chunks und Relevanzscores\n\n"
                + (
                    "\n\n---\n\n".join(chunks_block)
                    if chunks_block
                    else "Keine Chunks gefunden."
                )
            )

            return (
                f"## Antwort\n\n{answer}",
                details_markdown,
            )

        except Exception:
            logger.exception("Fehler bei der Anfrage.")

            return (
                "Die Anfrage konnte nicht verarbeitet werden. "
                "Bitte die Fehlermeldung im Terminal prüfen.",
                "",
            )

    with gr.Blocks(title="Solid Local RAG") as demo:
        gr.Markdown(
            "# Local LangChain RAG\n"
            "Lade ein PDF hoch und stelle Fragen an das Dokument. "
            "Die Anwendung läuft lokal mit LangChain, ChromaDB und Ollama."
        )

        # PDF-Upload und Indexierung.
        gr.Markdown("## 1. PDF hochladen und indexieren")

        pdf_file = gr.File(
            label="PDF auswählen",
            file_types=[".pdf"],
            type="filepath",
        )

        upload_button = gr.Button(
            "PDF indexieren",
            variant="primary",
        )

        upload_status = gr.Textbox(
            label="Indexierungsstatus",
            interactive=False,
        )

        upload_button.click(
            fn=upload_pdf,
            inputs=pdf_file,
            outputs=upload_status,
        )

        # Fragen und Antworten.
        gr.Markdown("## 2. Fragen an das Dokument")

        question = gr.Textbox(
            label="Frage",
            placeholder="Stelle eine Frage zum hochgeladenen PDF ...",
            lines=3,
        )

        mode = gr.Radio(
            choices=["similarity", "mmr", "threshold"],
            value=cfg.retriever_mode,
            label="Retriever-Modus",
        )

        submit = gr.Button(
            "Frage stellen",
            variant="primary",
        )

        output = gr.Markdown(
            label="Antwort",
        )

        details_output = gr.Markdown(
            label="Quellen, Chunks und Scores",
        )

        submit.click(
            fn=ask,
            inputs=[question, mode],
            outputs=[output, details_output],
        )

    return demo

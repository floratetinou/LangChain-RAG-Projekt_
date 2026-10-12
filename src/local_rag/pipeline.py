
import logging

from langchain_ollama import ChatOllama

from .config import Settings
from .prompts import RAG_PROMPT
from .retrievers import build_retriever
from .retry import ollama_retry
logger = logging.getLogger(__name__)


def _source_label(doc) -> str:
    """Erstellt eine lesbare Quellenangabe."""
    name = doc.metadata.get(
        "file_name",
        doc.metadata.get("source", "Unbekannt"),
    )

    page = doc.metadata.get("page")
    header = (
        doc.metadata.get("header_2")
        or doc.metadata.get("header_1")
    )

    parts = [str(name)]

    if page is not None:
        parts.append(f"Seite {int(page) + 1}")

    if header:
        parts.append(str(header))

    return " – ".join(parts)


def _document_key(doc) -> tuple:
    """Erstellt einen Schlüssel zum Zuordnen eines Chunks."""
    return (
        doc.page_content,
        doc.metadata.get("file_name"),
        doc.metadata.get("page"),
        doc.metadata.get("start_index"),
    )


def answer_question_with_details(
    question: str,
    mode: str,
    vectorstore,
    cfg: Settings,
) -> tuple[str, list[str], list[dict]]:
    """Gibt die Antwort, Quellen und Retrieval-Details zurück."""

    logger.info("Neue Anfrage mit Retriever-Modus: %s", mode)

    # Dokumente mit der ausgewählten Strategie abrufen.
    retriever = build_retriever(vectorstore, mode, cfg)
    docs = retriever.invoke(question)

    if not docs:
        logger.info("Keine passenden Dokumente gefunden.")
        return (
            "Die Wissensbasis enthält keine ausreichend passende Information.",
            [],
            [],
        )

    # Relevanzscores der ähnlichsten Dokumente ermitteln.
    candidate_k = max(cfg.retriever_k, cfg.mmr_fetch_k)

    scored_docs = vectorstore.similarity_search_with_relevance_scores(
        question,
        k=candidate_k,
    )

    score_lookup = {
        _document_key(doc): score
        for doc, score in scored_docs
    }

    # Retrieval-Details für die Benutzeroberfläche vorbereiten.
    details = []

    for doc in docs:
        score = score_lookup.get(_document_key(doc))

        details.append({
            "source": _source_label(doc),
            "score": score,
            "content": doc.page_content,
        })

    # Nur die gefundenen Chunks werden als Kontext verwendet.
    context = "\n\n".join(
        f"[Quelle: {_source_label(doc)}]\n{doc.page_content}"
        for doc in docs
    )

    llm = ChatOllama(
        model=cfg.llm_model,
        base_url=cfg.ollama_base_url,
        temperature=0,
    )
    chain = RAG_PROMPT | llm
    response = ollama_retry(cfg.retry_attempts)(
         chain.invoke
    )({
        "context": context,
        "question": question,
    })

    sources = list(dict.fromkeys(
        _source_label(doc) for doc in docs
    ))

    logger.info(
        "Anfrage erfolgreich beantwortet. Gefundene Chunks: %s",
        len(docs),
    )

    return response.content, sources, details


def answer_question(
    question: str,
    mode: str,
    vectorstore,
    cfg: Settings,
) -> tuple[str, list[str]]:
    """Kompatible Schnittstelle für bestehende Aufrufer."""
    answer, sources, _ = answer_question_with_details(
        question,
        mode,
        vectorstore,
        cfg,
    )

    return answer, sources

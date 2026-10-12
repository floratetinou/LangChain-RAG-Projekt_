from langchain_ollama import ChatOllama
from .config import Settings
from .prompts import RAG_PROMPT
from .retrievers import build_retriever


def _source_label(doc) -> str:
    name = doc.metadata.get("file_name", doc.metadata.get("source", "Unbekannt"))
    page = doc.metadata.get("page")
    header = doc.metadata.get("header_2") or doc.metadata.get("header_1")
    parts = [str(name)]
    if page is not None:
        parts.append(f"Seite {int(page) + 1}")
    if header:
        parts.append(str(header))
    return " – ".join(parts)


def answer_question(question: str, mode: str, vectorstore, cfg: Settings) -> tuple[str, list[str]]:
    """Grundpipeline. In einer späteren Lernstufe ergänzen wir LCEL und Retry feiner."""
    retriever = build_retriever(vectorstore, mode, cfg)
    docs = retriever.invoke(question)
    if not docs:
        return "Die Wissensbasis enthält keine ausreichend passende Information.", []

    context = "\n\n".join(
        f"[Quelle: {_source_label(doc)}]\n{doc.page_content}" for doc in docs
    )
    llm = ChatOllama(model=cfg.llm_model, base_url=cfg.ollama_base_url, temperature=0)
    response = (RAG_PROMPT | llm).invoke({"context": context, "question": question})
    sources = list(dict.fromkeys(_source_label(doc) for doc in docs))
    return response.content, sources

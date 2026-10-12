from .config import Settings

def build_retriever(vectorstore, mode: str, cfg: Settings):
    mode = mode.lower().strip()
    if mode == "similarity":
        return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": cfg.retriever_k})
    if mode == "mmr":
        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": cfg.retriever_k, "fetch_k": cfg.mmr_fetch_k},
        )
    if mode == "threshold":
        return vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": cfg.retriever_k, "score_threshold": cfg.score_threshold},
        )
    raise ValueError(f"Unbekannter Retriever-Modus: {mode}")

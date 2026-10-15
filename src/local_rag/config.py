from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embedding_model: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    llm_model: str = os.getenv("OLLAMA_LLM_MODEL", "llama3.2")
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))
    chroma_dir: Path = Path(os.getenv("CHROMA_DIR", "./chroma_db"))
    collection_name: str = os.getenv("CHROMA_COLLECTION", "local_rag_documents")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    retriever_mode: str = os.getenv("RETRIEVER_MODE", "similarity")
    retriever_k: int = int(os.getenv("RETRIEVER_K", "8"))
    mmr_fetch_k: int = int(os.getenv("MMR_FETCH_K", "12"))
    score_threshold: float = float(os.getenv("SCORE_THRESHOLD", "0.65"))
    retry_attempts: int = int(os.getenv("OLLAMA_RETRY_ATTEMPTS", "3"))
    gradio_host: str = os.getenv("GRADIO_HOST", "127.0.0.1")
    gradio_port: int = int(os.getenv("GRADIO_PORT", "7860"))

settings = Settings()

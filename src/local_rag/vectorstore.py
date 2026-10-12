from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from .config import Settings

def create_embeddings(cfg: Settings) -> OllamaEmbeddings:
    return OllamaEmbeddings(model=cfg.embedding_model, base_url=cfg.ollama_base_url)

def open_vectorstore(cfg: Settings) -> Chroma:
    cfg.chroma_dir.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=cfg.collection_name,
        embedding_function=create_embeddings(cfg),
        persist_directory=str(cfg.chroma_dir),
    )

#def index_documents(vectorstore: Chroma, documents) -> int:
    #if not documents:
        #return 0
   # vectorstore.add_documents(documents)
    #return len(documents)

def index_documents(vectorstore: Chroma, documents) -> int:

    if not documents:
        return 0

    print("\n===== CHUNKS AVANT INDEXATION =====")

    for i, doc in enumerate(documents, start=1):

        print("\n" + "=" * 50)
        print(f"Chunk {i}")

        print("\nMetadata:")
        print(doc.metadata)

        print("\nTexte:")
        print(doc.page_content[:200])

    vectorstore.add_documents(documents)

    return len(documents)

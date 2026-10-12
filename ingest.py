from src.local_rag.config import settings
from src.local_rag.loaders import load_directory
from src.local_rag.splitter import split_documents
from src.local_rag.vectorstore import open_vectorstore, index_documents


def main():
    documents = load_directory(settings.data_dir)
    chunks = split_documents(documents, settings.chunk_size, settings.chunk_overlap)
    store = open_vectorstore(settings)
    count = index_documents(store, chunks)
    print(f"Fertig: {count} Chunks wurden in Chroma indexiert.")

if __name__ == "__main__":
    main()

from pathlib import Path

from src.local_rag.loaders import load_file
from src.local_rag.splitter import split_documents

docs = load_file(Path("data/beispiel_wissensbasis.md"))

chunks = split_documents(
    docs,
    chunk_size=250,
    chunk_overlap=40
)

print(f"\nAnzahl Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):

    print("\n" + "=" * 60)
    print(f"Chunk {i+1}")
    print("=" * 60)

    print("\nMetadata:")
    print(chunk.metadata)

    print("\nText:")
    print(chunk.page_content)
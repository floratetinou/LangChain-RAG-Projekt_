from src.local_rag.config import settings
from src.local_rag.vectorstore import open_vectorstore
from src.local_rag.retrievers import build_retriever

# Ouvre Chroma
store = open_vectorstore(settings)

# Crée le retriever
retriever = build_retriever(
    store,
    mode="similarity",
    cfg=settings
)

# Question
question = "What is DoIP?"

print(f"\nQuestion: {question}")

docs = retriever.invoke(question)

print(f"\nTrouvé {len(docs)} document(s)\n")

for i, doc in enumerate(docs, start=1):

    print("=" * 60)
    print(f"Document {i}")

    print("\nMetadata:")
    print(doc.metadata)

    print("\nTexte:")
    print(doc.page_content)
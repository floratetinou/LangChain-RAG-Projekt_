from src.local_rag.config import settings
from src.local_rag.vectorstore import create_embeddings

embeddings = create_embeddings(settings)

vector = embeddings.embed_query(
    "What is DoIP?"
)

print(type(vector))
print(len(vector))

print("\nPremières valeurs :")
print(vector[:10])
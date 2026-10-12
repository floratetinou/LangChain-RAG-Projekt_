
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings
from langchain_chroma import Chroma

from src.local_rag.vectorstore import rebuild_index


def test_rebuild_index_with_real_chroma(tmp_path):
    """Prüft den Neuaufbau einer echten Chroma-Collection."""

    # Eine echte Chroma-Collection für den Test erstellen.
    store = Chroma(
        collection_name="test_rebuild_index",
        embedding_function=FakeEmbeddings(size=8),
        persist_directory=str(tmp_path / "chroma_test"),
    )

    # Zuerst alte Testdaten indexieren.
    store.add_documents([
        Document(page_content="Alter Testinhalt")
    ])

    # Den Index mit neuen Testdaten neu aufbauen.
    new_documents = [
        Document(page_content="DoIP nutzt Ethernet."),
        Document(page_content="DoIP dient der Fahrzeugdiagnose."),
    ]

    count = rebuild_index(store, new_documents)

    # Prüfen, ob die neuen Dokumente im Index liegen.
    results = store.similarity_search("DoIP Fahrzeugdiagnose", k=5)
    contents = [doc.page_content for doc in results]

    assert count == 2
    assert "Alter Testinhalt" not in contents
    assert set(contents) == {
        "DoIP nutzt Ethernet.",
        "DoIP dient der Fahrzeugdiagnose.",
    }

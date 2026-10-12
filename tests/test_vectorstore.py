
from unittest.mock import Mock

import pytest
from langchain_core.documents import Document

from src.local_rag.vectorstore import index_documents, rebuild_index


def test_index_documents_adds_documents():
    """Prüft, ob Dokumente zum Vektorindex hinzugefügt werden."""

    vectorstore = Mock()
    documents = [
        Document(page_content="DoIP ist ein Diagnoseprotokoll."),
        Document(page_content="DoIP nutzt IP-Netzwerke."),
    ]

    count = index_documents(vectorstore, documents)

    assert count == 2
    vectorstore.add_documents.assert_called_once_with(documents)


def test_index_documents_returns_zero_for_empty_list():
    """Prüft, ob eine leere Liste ohne Indexierung behandelt wird."""

    vectorstore = Mock()

    count = index_documents(vectorstore, [])

    assert count == 0
    vectorstore.add_documents.assert_not_called()


def test_rebuild_index_resets_and_adds_documents():
    """Prüft, ob der Index zurückgesetzt und neu aufgebaut wird."""

    vectorstore = Mock()
    documents = [
        Document(page_content="DoIP verwendet Ethernet."),
        Document(page_content="DoIP unterstützt Fahrzeugdiagnose."),
    ]

    count = rebuild_index(vectorstore, documents)

    assert count == 2
    vectorstore.reset_collection.assert_called_once_with()
    vectorstore.add_documents.assert_called_once_with(documents)


def test_rebuild_index_rejects_empty_list():
    """Prüft, ob ein Neuaufbau mit einer leeren Liste abgelehnt wird."""

    vectorstore = Mock()

    with pytest.raises(ValueError, match="leeren Dokumentliste"):
        rebuild_index(vectorstore, [])

    vectorstore.reset_collection.assert_not_called()
    vectorstore.add_documents.assert_not_called()

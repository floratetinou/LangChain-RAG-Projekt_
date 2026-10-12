from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

HEADERS = [("#", "header_1"), ("##", "header_2"), ("###", "header_3")]

def split_documents(documents: list[Document], chunk_size: int, chunk_overlap: int) -> list[Document]:
    """Teilt Markdown zuerst nach Überschriften und danach alle Dokumente rekursiv."""
    intermediate: list[Document] = []
    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS, strip_headers=False)
    for doc in documents:
        if doc.metadata.get("file_type") == "md":
            sections = md_splitter.split_text(doc.page_content)
            for section in sections:
                section.metadata = {**doc.metadata, **section.metadata}
            intermediate.extend(sections)
        else:
            intermediate.append(doc)

    recursive = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True,
    )
    return recursive.split_documents(intermediate)

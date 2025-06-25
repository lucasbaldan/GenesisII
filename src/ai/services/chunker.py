from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunker(doc: list[Document]) -> list[Document]:
    """
    Faz o chunker do conteúdo do documento conforme as regras definidas nessa função.
    """
    chunk_min_chars: int = 30
    chunk_size: int = 850
    chunk_overlap: int = 100

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(doc)

    chunks_sanitized = [chunk for chunk in chunks if len(chunk.page_content.strip()) >= chunk_min_chars]

    return chunks_sanitized

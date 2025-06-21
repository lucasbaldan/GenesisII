from http import HTTPStatus
import mimetypes
from fastapi import APIRouter, HTTPException
from langchain_unstructured import UnstructuredLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path

from src.ai.tools.FAISS import salvar_doc_faiss


router = APIRouter(prefix="/archive", tags=["arquive"])

@router.post("/", status_code=HTTPStatus.OK)
async def cadastrar_archive(caminho_arquivo="chamada2024.pdf"):
    """
    Endpoint para processamentos de documentos pela IA.
    Guarda o documento vetorizado no banco FAISS.    
    """
    chunk_min_chars: int = 30
    chunk_size: int = 1000
    chunk_overlap: int = 100
    try:
        if not Path(caminho_arquivo).exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        
        documento = UnstructuredPDFLoader(caminho_arquivo).load()

        for doc in documento:
            linhas = doc.page_content.splitlines()
            doc.page_content = " ".join(linha.strip() for linha in linhas if linha.strip())

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(documento)

        chunks_sanitized = [chunk for chunk in chunks if len(chunk.page_content.strip()) >= chunk_min_chars]

        result = salvar_doc_faiss(Path(caminho_arquivo).name, chunks_sanitized)
        
        if result:
           raise HTTPException(status_code=500, detail=str(result)) 

        return {"message": "Documento processado com sucesso", "tipo_documento": mimetypes.guess_type(caminho_arquivo)[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

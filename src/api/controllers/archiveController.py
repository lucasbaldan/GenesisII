from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from langchain_unstructured import UnstructuredLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path

import os

from src.ai.tools.FAISS import salvar_doc_faiss


router = APIRouter(prefix="/archive", tags=["arquive"])

@router.post("/", status_code=HTTPStatus.OK)
async def cadastrar_archive(caminho_arquivo="chamada2024.pdf"):
    """
    Endpoint para processamentos de documentos pela IA.
    Guarda o documento vetorizado no banco FAISS.    
    """
    chunk_min_chars: int = 30
    chunk_size: int = 2000
    chunk_overlap: int = 100
    try:
        if not Path(caminho_arquivo).exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        
        documento = UnstructuredLoader(caminho_arquivo).load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(documento)

        chunks_sanitized = [chunk for chunk in chunks if len(chunk.page_content.strip()) >= chunk_min_chars]

        # result = salvar_doc_faiss(Path(caminho_arquivo).name, chunks)
        
        # if result:
        #    raise HTTPException(status_code=500, detail=str(result)) 

        print([chunk.page_content for chunk in chunks_sanitized]) 

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from http import HTTPStatus
import mimetypes
from fastapi import APIRouter, HTTPException
from src.ai.services.docsLoaders import DocsLoaders
from pathlib import Path

from src.ai.tools.FAISS import salvar_doc_faiss
from src.ai.services.chunker import chunker


router = APIRouter(prefix="/archive", tags=["archive"])

@router.post("/", status_code=HTTPStatus.OK)
async def cadastrar_archive(caminho_arquivo="chamada2024.pdf"):
    """
    Endpoint para processamentos de documentos pela IA.
    Guarda o documento vetorizado no banco FAISS.    
    """
    try:
        loader = DocsLoaders(caminho_arquivo)
        if loader.loaderErrors:
            raise HTTPException(status_code=400, detail=loader.loaderErrors)
        
        match loader.extensao:
            case ".pdf":
                loader.PDFLoader()
            case ".docx":
                loader.MSWordLoader()
            case ".pptx":
                loader.MSPowerPointLoader()
            case ".txt":
                loader.TxtLoader()
            case _:
                raise HTTPException(status_code=400, detail=f"Tipo de arquivo não suportado: {loader.extensao}. Apenas arquivos com extensão .pdf, .docx, .pptx, .txt são suportados.")
            
        if not loader.result or len(loader.result) < 1:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao processar o documento. Verifique se o arquivo contém conteúdo válido.")
        
        chunk = chunker(loader.result)
        
        result = salvar_doc_faiss(loader.nome, chunk)
        print(result)

        return {"message": "Documento processado com sucesso", "tipo_documento": loader.extensao, "nome_documento": loader.nome}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

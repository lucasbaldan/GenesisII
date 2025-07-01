from http import HTTPStatus
from operator import or_
import traceback
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.services.docsLoaders import DocsLoaders
from src.ai.tools.FAISS import salvar_doc_faiss
from src.ai.services.chunker import chunker
from src.api.database.models import ProcessedDocs

from src.api.database.engine import get_session_engine

router = APIRouter(prefix="/archive", tags=["archive"])

@router.post("/", status_code=HTTPStatus.OK)
async def cadastrar_archive(caminho_arquivo="chamada2024.pdf",
                            titulo_documento: str="Chamada 2024",
                            descricao_documento: str="Documento de chamada 2024",
                            session: AsyncSession = Depends(get_session_engine)):
    """
    Endpoint para processamentos de documentos pela IA.
    Guarda o documento vetorizado no banco FAISS.    
    """
    try:
        loader = DocsLoaders(caminho_arquivo)
        if loader.loaderErrors:
            raise HTTPException(status_code=400, detail=loader.loaderErrors)
        
        verifica_doc_db = await session.execute(
            select(ProcessedDocs).where(
                or_(
                    ProcessedDocs.nome_arquivo == loader.nome,
                    ProcessedDocs.nome_documento == titulo_documento
                )
            ).limit(1)
        )
        doc_db = verifica_doc_db.scalar_one_or_none()
        
        if doc_db:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Ja existe um documento com o mesmo título e/ou arquivo cadastrado na plataforma. Por favor, revise o arquivo.")

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
              
        chunk = chunker(loader.result)
        
        doc_ids = salvar_doc_faiss(loader.nome, chunk)

        novo_doc_sql = ProcessedDocs(
            usuario_id=1,
            nome_arquivo=loader.nome,
            nome_documento=titulo_documento,
            descricao=descricao_documento,
            faiss_ids=doc_ids
        )

        session.add(novo_doc_sql)
        await session.commit()

        return {"message": "Documento processado com sucesso", "tipo_documento": loader.extensao, "nome_documento": loader.nome}

    except Exception as e:
        print(f"Erro ao processar o documento: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

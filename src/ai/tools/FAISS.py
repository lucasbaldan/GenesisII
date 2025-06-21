import datetime

import os

from typing import List
import uuid

from langchain_community.vectorstores import FAISS # Para armazenar os embeddings
from langchain_core.tools import tool # Decorador para definir ferramentas
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

from dotenv import load_dotenv
load_dotenv()

caminho_faiss = os.getenv("FAISS_PATH")

embedding_model = OpenAIEmbeddings()

if os.path.exists(caminho_faiss):
    faiss = FAISS.load_local(caminho_faiss, embedding_model, allow_dangerous_deserialization=True)
else:
    documentos = [
        Document(
            page_content="...",
            metadata={"id": str(uuid.uuid4()), "data": "2025-05-02", "tipo": "teste"}
        )
    ]
    faiss = FAISS.from_documents(documentos, embedding_model)
    faiss.save_local(caminho_faiss)


@tool
def atualizar_info_faiss(doc_id: str, novo_texto: str) -> str | None:
    """
    Exclui uma informação Salva no banco vetorial FAISS que está desatualizada e adiciona a nova informação atualização para uso futuro.

    Parâmetros:
    - doc_id: o ID do documento FAISS a ser deletado.
    - texto: o conteúdo atualizado a ser registrado.

    """
    try:
        old_doc = faiss.get_by_ids([doc_id])
        if not old_doc:
            return (f"Registro de memória não encontrado para o ID informado.")

        # Deletar o documento original
        faiss.delete([doc_id])

        documento_atualizado = Document(
            page_content=novo_texto,
            metadata={
                "id": doc_id,
                "tipo": old_doc[0].metadata.get("tipo", "desconhecido"),
                "data": datetime.datetime.now().strftime("%Y-%m-%d")
            }
        )

        faiss.add_documents([documento_atualizado], ids=[doc_id]) # Adicionar o novo documento ao índice
        faiss.save_local(caminho_faiss)
    
    except Exception as e:
        return(f"Erro ao atualizar a informação no FAISS: {e}")




@tool
def salvar_info_faiss(texto: str, tipo: str) -> str | None:
    """
    Salva uma nova informação útil no banco vetorial FAISS para uso futuro.

    Parâmetros:
    - texto: o conteúdo informativo a ser registrado.
    - tipo: a categoria da informação. Deve ser uma palavra-chave como 'contato', 'estrutura', 'procedimento', etc.

    A IA deve inferir o tipo com base no conteúdo da informação.
    """
    try:
        doc_id = str(uuid.uuid4())  # Gerar um ID único para a memória

        documento = Document(
            page_content=texto,
            metadata={
                "id": doc_id,
                "tipo": tipo,
                "data": datetime.datetime.now().strftime("%Y-%m-%d")
            }
        )
        faiss.add_documents([documento], ids=[doc_id])
        faiss.save_local(caminho_faiss)
    
    except Exception as e:
        return(f"Erro ao salvar a informação no FAISS: {e}")
    


def salvar_doc_faiss(nome_doc: str, chunks_doc: List[Document]) -> str | None:
    """
    Salva um chunck de documento no banco vetorial FAISS para uso futuro.
    """
    try:
        metadata_clear= {"id", "doc", "chunk_id", "data", "filename", "page_number", 'filetype', 'category'}
        
        doc_ids = []

        for i, chunk in enumerate(chunks_doc):
            
            uid = str(uuid.uuid4())
            doc_ids.append(uid)

            chunk.metadata.update({
                "id": uid,
                "doc": nome_doc,
                "chunk_id": i,
                "data": datetime.datetime.now().strftime("%Y-%m-%d")
            })

            chunk.metadata = {k: v for k, v in chunk.metadata.items() if k in metadata_clear}


        print(chunks_doc)

        # faiss.add_documents(chunks_doc, ids=doc_ids)
        # faiss.save_local(caminho_faiss)

        return None
    
    except Exception as e:
        return f"Erro ao salvar documento no FAISS :-> {e}"
    


@tool
def buscar_info_faiss(pergunta_usuario: str) -> list[dict] | None | str:
    """
    Busca as informações mais relevantes no índice FAISS com base na pergunta feita pelo usuário.
    Retorna uma lista de dicionários contendo conteúdo, id e metadados.
    
    """
    try:
        resultados = faiss.similarity_search_with_score(pergunta_usuario, k=10)
        if resultados:
            return [
                {
                    "doc_id": r.metadata.get("id", "idnull"),
                    "page_content": r.page_content,
                    "score": score
                }
                for r, score in resultados if score < 1.5
            ]
        else:
            return None
    
    except Exception as e:
        return(f"Erro ao buscar informações no FAISS: {e}")
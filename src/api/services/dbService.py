from sqlalchemy import desc, select

from src.api.database.engine import get_session_engine_context
from src.api.database.models import AgentMemory, ProcessedDocs, HistoricoChat

# FUNÇÕES UTILIZADAS DENTRO DAS TOOLS DA IA PARA GRAVAR INFOs NO BANCO SQL

async def salvar_nova_memoria(texto: str, doc_id: str) -> str | None:
    try:
        # 2. Criar conexão e salvar no SQL
        async with get_session_engine_context() as session:
            nova_memoria = AgentMemory(
                descricao_memoria=texto,
                faiss_id=doc_id,
                usuario_id=1 
            )
            session.add(nova_memoria)
            await session.commit()

        return None

    except Exception as e:
        print (f"Erro ao salvar memória no banco -> {e}")
        return f"Erro ao salvar memória no banco de dados: {e}"
    

async def atualiza_memoria(novo_texto: str, doc_id: str) -> str | None:
    try:
        async with get_session_engine_context() as session:
            if doc_id:
                verifica_memoria = await session.execute(
                    select(AgentMemory).where(AgentMemory.faiss_id == doc_id).limit(1)
                )
                memoria = verifica_memoria.scalar_one_or_none()

                if memoria:
                    memoria.ativo = False
                    memoria.faiss_id = None
                else: 
                    print (f"Registro de memória não encontrado - ID: {doc_id}")
        nova_memoria = AgentMemory(
            descricao_memoria=novo_texto,
            faiss_id=doc_id,
            usuario_id=1 
        )
        session.add(nova_memoria)
        await session.commit()

        return None

    except Exception as e:
        print (f"Erro ao salvar memória no banco -> {e}")
        return f"Erro ao salvar memória no banco de dados: {e}"
    

# FUNCTIONS FOR DOCS.

async def salvar_novo_doc(filename: str, doc_ids: list[str]) -> str | None:
    try:
        # 2. Criar conexão e salvar no SQL
        async with get_session_engine_context() as session:
            novo_doc = ProcessedDocs(
                titulo_doc=filename,
                faiss_ids=doc_ids,
                usuario_id=1
            )
            session.add(novo_doc)
            await session.commit()

        return None

    except Exception as e:
        print (f"Erro ao salvar memória no banco -> {e}")
        return f"Erro ao salvar memória no banco de dados: {e}"
    

# FUNCTIONS FOR CHAT_HISTORY.
    
async def getHistoryChatByThreadID(thread_id: str) -> str | None:
    try:
        # 2. Criar conexão e consultar no SQL
        async with get_session_engine_context() as session:
            result = await session.execute(
                select(HistoricoChat)
                .where(HistoricoChat.thread_id == thread_id)
                .order_by(desc(HistoricoChat.created_at))
                .limit(30)
        )
        mensagens = result.scalars().all()

        return None

    except Exception as e:
        print (f"Erro ao salvar memória no banco -> {e}")
        return f"Erro ao salvar memória no banco de dados: {e}"
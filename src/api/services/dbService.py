from src.api.database.engine import get_session_engine_context
from src.api.database.models import AgentMemory

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
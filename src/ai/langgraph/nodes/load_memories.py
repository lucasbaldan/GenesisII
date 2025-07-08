from typing import Dict, Any

from sqlalchemy import desc, select

from src.api.database.engine import get_session_engine_context
from src.api.database.models import HistoricoChat

async def carregar_memoria_chat(state: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Carrega o histórico de interações do usuário com o chat salvo no sql.
    O histórico é formatado como uma string, onde cada interação é separada por quebras, padrão mais reconhecidos pelos agents de ia.
    '''
    try:
        thread_id = state.get("thread_id", None)

        if not thread_id:
            return {"chat_history": ""}
        
        # Criar conexão e consultar no SQL
        async with get_session_engine_context() as session:
            result = await session.execute(
                select(HistoricoChat)
                .where(HistoricoChat.thread_id == thread_id)
                .order_by(desc(HistoricoChat.created_at))
                .limit(30)
        )
        mensagens = result.scalars().all()

        chat_history = ""
        for interacao in mensagens:
            chat_history += f"Usuário: {interacao.prompt_description if interacao.prompt_description else 'Prompt não reconhecido'}\n"
            chat_history += f"IA: {interacao.response_description if interacao.response_description else 'Response não reconhecido'}\n"

        print(f"Histórico Recuperado do chat -> {chat_history}")    
        return {"chat_history": chat_history}

    except Exception as e:
            print (f"Erro ao consultar histórico do chat -> {e}")
            return {"chat_history": ""}
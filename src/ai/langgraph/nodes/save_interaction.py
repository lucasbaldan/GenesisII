from typing import Dict, Any
import uuid

from sqlalchemy import asc, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models import HistoricoChat

async def salve_interaction_db(state: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Salva a interação do usuário com o chat no banco de dados.
    '''
    try:
        thread_id = state.get("thread_id", None)
        user_prompt = state.get("prompt", None)
        result_agent = state.get("resposta_agent", None)
        session: AsyncSession = state.get("session", None)

        chat_history = HistoricoChat(
            thread_id=thread_id if thread_id else str(uuid.uuid4()),
            prompt_description=user_prompt,
            response_description=result_agent,
            usuario_id=1,
            titulo_chat="Novo Chat" if not thread_id else None
        )
        session.add(chat_history)

        # ultima ação da sessão do banco dentro do grafo
        await session.commit()
        
        return { user_prompt: user_prompt }

    except Exception as e:
            print (f"Erro ao gravar histórico do chat -> {e}")
            raise Exception(f"Erro ao gravar histórico do chat -> {e}")
from typing import Dict, Any

from sqlalchemy import asc, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models import HistoricoChat, ChatResumes

import os
from dotenv import load_dotenv
load_dotenv()

MODEL = os.getenv("MODEL", 'gpt-3.5-turbo')
MAX_TOKENS = os.getenv("MAX_TOKENS", "4096")

async def carregar_memoria_chat(state: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Carrega o histórico de interações do usuário com o chat salvo no sql.
    O histórico é formatado como uma string, onde cada interação é separada por quebras, padrão mais reconhecidos pelos agents de ia.
    '''
    try:
        thread_id = state.get("thread_id", None)
        session: AsyncSession = state.get("session", None)

        if not thread_id:
            return {"chat_history": ""}
        if not session:
            raise Exception("Erro ao se comunicar com o banco de dados.")
        
        # Criar conexão e consultar no SQL
        result = await session.execute(
             select(HistoricoChat)
             .where(
                  and_(HistoricoChat.thread_id == thread_id,
                       HistoricoChat.compacted == False)
             )
             .order_by(asc(HistoricoChat.created_at))
        )
        mensagens = result.scalars().all()

        resumo = await session.execute(
             select(ChatResumes)
             .where(ChatResumes.thread_id == thread_id)
             .limit(1)
        )
        resumo = resumo.scalars().first()
        
        return {"chat_history": mensagens, "chat_resume": resumo}

    except Exception as e:
            print (f"Erro ao consultar histórico do chat -> {e}")
            raise Exception(f"Erro ao consultar histórico do chat -> {e}")
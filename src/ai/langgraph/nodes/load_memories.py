from datetime import datetime
from typing import Dict, Any
from zoneinfo import ZoneInfo

from langchain_core.messages import HumanMessage, AIMessage

from sqlalchemy import desc, select, and_

from src.api.database.engine import get_session_engine_context
from src.api.database.models import HistoricoChat, ChatResumes
from src.ai.langgraph.BaseAgent import model as llm

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

        if not thread_id:
            return {"chat_history": ""}
        
        # Criar conexão e consultar no SQL
        async with get_session_engine_context() as session:
            result = await session.execute(
                select(HistoricoChat)
                .where(
                 and_(HistoricoChat.thread_id == thread_id,
                      HistoricoChat.compacted == False)
                )
                .order_by(desc(HistoricoChat.created_at))
            )
            mensagens = result.scalars().all()

            chat_history = []
            for interacao in mensagens:
                chat_history.append(HumanMessage(content=interacao.prompt_description if interacao.prompt_description else 'Prompt não reconhecido'))
                chat_history.append(AIMessage(content=interacao.response_description if interacao.response_description else 'Response não reconhecido'))

            resumo = await session.execute(
                select(ChatResumes)
                .where(ChatResumes.thread_id == thread_id)
                .limit(1)
            )
            resumo = resumo.scalars().first()

            return {"chat_history": chat_history, "chat_resume": resumo.resume if resumo.resume else ''}


        return {"chat_history": chat_history}

    except Exception as e:
            print (f"Erro ao consultar histórico do chat -> {e}")
            return {"chat_history": ""}
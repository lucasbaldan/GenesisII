from datetime import datetime
from typing import Any, Dict
import uuid
import pytz

from langmem.short_term import SummarizationNode
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages import BaseMessage

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models import ChatResumes, HistoricoChat
from src.ai.langgraph.BaseAgent import model

from dotenv import load_dotenv
import os

async def checkAndSummary(state: Dict[str, Any]) -> Dict[str, Any]:
    load_dotenv()
    max_tokens = int(os.getenv("MAX_TOKENS", "4096")) * 0.70
    max_summary_tokens = int(os.getenv("MAX_TOKENS", "4096")) * 0.30
    resumo_atual: ChatResumes | None = state.get("chat_resume", None)
    historico: list[HistoricoChat] | None = state.get("chat_history", None)
    session: AsyncSession = state.get("session", None)

    try:
        if not historico or len(historico) < 2:
            return {"chat_resume": ""}
        
        chat_history: list[BaseMessage] = []
        for interacao in historico:
            chat_history.append(HumanMessage(content=interacao.prompt_description if interacao.prompt_description else 'Prompt não reconhecido', id=str(uuid.uuid4())))
            chat_history.append(AIMessage(content=interacao.response_description if interacao.response_description else 'Response não reconhecido', id=str(uuid.uuid4())))
        
        summarizer_node = SummarizationNode(
            model=model,
            input_messages_key="chat_history",
            output_messages_key="chat_resume",
            existing_summary_prompt=resumo_atual.resume if resumo_atual and resumo_atual.resume else "",
            max_tokens=max_tokens,
            max_summary_tokens=max_summary_tokens,
        )

        output = await summarizer_node.ainvoke({"chat_history": chat_history})
        novo_resumo: str | list = output["chat_resume"]

        if novo_resumo and isinstance(novo_resumo[0], SystemMessage) and novo_resumo[0].content.__contains__("Summary of the conversation"):
            if resumo_atual and resumo_atual.id:

                resumo_atual.resume = novo_resumo[0].content,
                resumo_atual.last_update = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
            
            else:
                resumo_atual = ChatResumes(thread_id=state.get("thread_id", "-1"), resume=novo_resumo[0].content)
                session.add(resumo_atual)
            
            for historico_item in historico[:-5]:
                historico_item.compacted = True

        return {"chat_resume": resumo_atual if resumo_atual else ""}

    except Exception as e:
        print(f"Erro ao gerar resumo: {e}")
        raise Exception(f"Erro ao gerar resumo: {e}")
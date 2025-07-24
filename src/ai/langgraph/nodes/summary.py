from typing import Any, Dict
from langmem.short_term import SummarizationNode
from langchain_core.messages import SystemMessage

from api.database.engine import get_session_engine_context
from api.database.models import ChatResumes
from src.ai.langgraph.BaseAgent import model

from dotenv import load_dotenv
import os

async def checkAndSummary(state: Dict[str, Any]) -> Dict[str, Any]:
    load_dotenv()
    #max_tokens = int(os.getenv("MAX_TOKENS", "4096")) * 0.70
    #max_summary_tokens = int(os.getenv("MAX_TOKENS", "4096")) * 0.30
    max_tokens = 120 * 0.70
    max_summary_tokens = 120 * 0.30
    resumo_atual = state.get("chat_resume", "")


    summarizer_node = SummarizationNode(
        model=model,
        input_messages_key="chat_history",
        output_messages_key="chat_resume",
        existing_summary_prompt=resumo_atual,
        max_tokens=max_tokens,
        max_summary_tokens=max_summary_tokens,
    )

    try:
        output = await summarizer_node.ainvoke(state)
        novo_resumo: str | list = output["chat_resume"]

        #print(f"\n\n RETORNO DO SUMMARY\n {novo_resumo}\n\n")

        if novo_resumo and isinstance(novo_resumo[0], SystemMessage) and novo_resumo[0].content.__contains__("Summary of the conversation"):
             async with get_session_engine_context() as session:
                session.add(ChatResumes(thread_id=state.get("thread_id"), resume=novo_resumo[0].content))
                await session.commit()
                return {"chat_resume": novo_resumo[0].content}
        else:
            return {"chat_resume": ""}

    except Exception as e:
        print(f"Erro ao gerar resumo: {e}")
        return {"resposta_agent": "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."}
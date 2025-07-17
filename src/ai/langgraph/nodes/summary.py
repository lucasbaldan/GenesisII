from typing import Any, Dict
from langmem.short_term import SummarizationNode
from langchain_core.messages.utils import count_tokens_approximately

from src.ai.langgraph.BaseAgent import model

from dotenv import load_dotenv
import os

async def checkAndSummary(state: Dict[str, Any]) -> Dict[str, Any]:
    load_dotenv()
    max_tokens = int(os.getenv("MAX_TOKENS", "2870")) * 0.70
    resumo_atual = state.get("chat_resume", "")


    summarizer_node = SummarizationNode(
        model=model,
        input_messages_key="chat_history",
        output_messages_key="chat_resume",
        existing_summary_prompt=resumo_atual,
        max_tokens=max_tokens
    )

    try:
        output = await summarizer_node.ainvoke(state)
        novo_resumo: str = output["chat_resume"]

        return {"chat_resume": novo_resumo}

    except Exception as e:
        print(f"Erro ao gerar resumo: {e}")
        return {"resposta_agent": "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."}
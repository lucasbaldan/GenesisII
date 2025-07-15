from typing import Any, Dict
from langmem.short_term import SummarizationNode

from src.ai.langgraph.BaseAgent import model as llm

async def checkAndSummary(state: Dict[str, Any]) -> Dict[str, Any]:

    summarizer_node = SummarizationNode(
        llm=llm,
        input_messages_key="chat_history",
        output_messages_key="chat_resume",
        existing_summary_prompt=""
    )

    try:
        output = await summarizer_node.ainvoke(state)
        novo_resumo = output["chat_resume"]

        return {"chat_resume": novo_resumo}

    except Exception as e:
        print(f"Erro ao gerar resumo: {e}")
        return {"resumo_gerado": ""}
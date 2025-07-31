from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models import ChatResumes, HistoricoChat
from src.ai.langgraph.nodes.exec_agent import exec_agent
from src.ai.langgraph.nodes.load_memories import carregar_memoria_chat
from src.ai.langgraph.nodes.prompt_factory import prompt_build
from src.ai.langgraph.nodes.summary import checkAndSummary
from src.ai.langgraph.nodes.save_interaction import salve_interaction_db


from typing import TypedDict

class AgentState(TypedDict):
    prompt: str
    thread_id: str
    chat_history: list[HistoricoChat] | None = None
    chat_resume: ChatResumes | None = None
    resposta_agent: str
    final_prompt: str
    session: AsyncSession

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("load_memories_chat", carregar_memoria_chat)
    workflow.add_node("summary", checkAndSummary)
    workflow.add_node("prompt_build", prompt_build)
    workflow.add_node("exec_agent", exec_agent)
    workflow.add_node("save_interaction", salve_interaction_db)    

    workflow.set_entry_point("load_memories_chat")
    workflow.add_edge("load_memories_chat", "summary")
    workflow.add_edge("summary", "prompt_build")
    workflow.add_edge("prompt_build", "exec_agent")
    workflow.add_edge("exec_agent", "save_interaction")
    workflow.add_edge("save_interaction", END)

    return workflow.compile()

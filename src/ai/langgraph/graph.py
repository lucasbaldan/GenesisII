from langgraph.graph import StateGraph, END
from src.ai.langgraph.nodes.exec_agent import exec_agent

from typing import TypedDict

class AgentState(TypedDict):
    prompt: str
    thread_id: str
    chat_history: str
    resposta_agent: str

def build_graph():
    workflow = StateGraph(AgentState)

    #workflow.add_node("carregar_memoria", carregar_memoria_sql)
    workflow.add_node("exec_agent", exec_agent)
    #workflow.add_node("salvar", salvar_interacao)

    workflow.set_entry_point("exec_agent")
    #workflow.add_edge("carregar_memoria", "executar_agente")
    #workflow.add_edge("executar_agente", "salvar")
    workflow.add_edge("exec_agent", END)

    return workflow.compile()

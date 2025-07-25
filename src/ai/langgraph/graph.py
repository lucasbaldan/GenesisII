from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
from src.ai.langgraph.nodes.exec_agent import exec_agent
from src.ai.langgraph.nodes.load_memories import carregar_memoria_chat
from src.ai.langgraph.nodes.prompt_factory import prompt_build
from src.ai.langgraph.nodes.summary import checkAndSummary


from typing import TypedDict

class AgentState(TypedDict):
    prompt: str
    thread_id: str
    chat_history: list[BaseMessage]
    chat_history_str: str
    chat_resume: str
    resposta_agent: str
    final_prompt: str

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("load_memories_chat", carregar_memoria_chat)
    workflow.add_node("summary", checkAndSummary)
    workflow.add_node("prompt_build", prompt_build)
    workflow.add_node("exec_agent", exec_agent)

    workflow.set_entry_point("load_memories_chat")
    workflow.add_edge("load_memories_chat", "summary")
    workflow.add_edge("summary", "prompt_build")
    workflow.add_edge("prompt_build", "exec_agent")
    workflow.add_edge("exec_agent", END)

    return workflow.compile()

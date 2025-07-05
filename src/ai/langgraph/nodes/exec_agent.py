import traceback
from typing import Any, Dict
from langchain.schema import AIMessage


from src.ai.langgraph.BaseAgent import graph

async def exec_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    chat_history = state.get("chat_history", "")
    user_input = state["prompt"]  # Obtém a entrada do usuário do estado

    try:
        resultado = await graph.ainvoke(
            input={"messages": user_input}
        )

        print(f"Resultado do agente: {resultado}")
        
        for msg in reversed(resultado["messages"]):
            if isinstance(msg, AIMessage) and msg.content.strip():
                return {"resposta_agent": msg.content.strip()} 
        return {"resposta_agent": "Me perdoe, não consegui encontrar uma resposta adequada para sua pergunta."}
        
    except Exception as e:
        print(f"Erro ao executar o agente: {e}")
        traceback.print_exc()
        return {"resposta_agent": "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."}
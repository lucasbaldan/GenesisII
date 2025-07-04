import traceback
from typing import Any, Dict


from src.ai.langgraph.BaseAgent import graph

async def exec_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    chat_history = state.get("chat_history", "")
    user_input = state["prompt"]  # Obtém a entrada do usuário do estado

    # Adiciona o histórico ao input como contexto (isso depende de como sua prompt foi criada)
    # entrada_final = f"{chat_history}\nUsuário: {user_input}"

    try:
        resultado = await graph.ainvoke(
            {"input": user_input}
        )
        
        mensagens = resultado.get("messages", [])
        
        if not mensagens or not hasattr(mensagens[0], "content"):
            raise ValueError("Resposta do agente não encontrada ou inválida.")
        
        return {"resposta_agent": mensagens[0].content}
        
    except Exception as e:
        print(f"Erro ao executar o agente: {e}")
        traceback.print_exc()
        return {"resposta_agent": "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."}
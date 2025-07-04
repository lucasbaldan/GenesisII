from typing import Dict, Any

async def carregar_memoria_sql(state: Dict[str, Any]) -> Dict[str, Any]:
    user_id = state["user_id"]
    
    #historico = await get_ultimos_turnos_do_usuario(user_id=user_id, limite=5)

    chat_history = ""
    for interacao in []:
        chat_history += f"Usuário: {interacao.prompt_description}\n"
        chat_history += f"IA: {interacao.response_description}\n"

    return {"chat_history": chat_history}
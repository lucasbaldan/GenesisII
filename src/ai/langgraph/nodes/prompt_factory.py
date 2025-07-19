import textwrap
from typing import Dict, Any

from langchain_core.messages import HumanMessage, AIMessage

def prompt_build(state: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Utiliza o histórico do chat carregado e monta o prompt final a ser processado pelo agente de IA.
    '''
    chat_resume = state.get("chat_resume", None)
    historico_chat = state.get("chat_history", None)
    user_question = state.get("prompt", None)

    print(state)

    final_prompt = ""

    if chat_resume:
        final_prompt += f"---RESUMO DO HISTÓRICO DO CHAT COM O USUÁRIO--- \n {chat_resume} \n\n"

    if historico_chat:
        final_prompt += f"---HISTÓRICO RECENTE DO CHAT---: \n "
        for historico in historico_chat[-10:]:
            if isinstance(historico, HumanMessage):
                final_prompt += f"USUÁRIO: {historico.content.replace('\n', '').replace('\r', '')} \n"
            elif isinstance(historico, AIMessage):
                final_prompt += f"IA: {historico.content.replace('\n', '').replace('\r', '')} \n"
        
        final_prompt += "\n"

    final_prompt += f"---INPUT DO USUÁRIO: {user_question}"

    final_prompt = textwrap.dedent(final_prompt)  # Remove indentations for better formatting
    
    return {"final_prompt": final_prompt}
    

    
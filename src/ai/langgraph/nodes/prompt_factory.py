import textwrap
from typing import Dict, Any

def prompt_build(state: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Utiliza o histórico do chat carregado e monta o prompt final a ser processado pelo agente de IA.
    '''
    chat_resume = state.get("chat_resume", None)
    historico_chat = state.get("chat_history", None)
    user_question = state.get("prompt", None)

    final_prompt = ""

    if chat_resume:
        final_prompt += f"---RESUMO DOS INTERESSES DO USUÁRIO COM A IA---: \n {chat_resume} \n"

    if historico_chat:
        final_prompt += f"---HISTÓRICO DO CHAT---: \n {historico_chat} \n"
    
    final_prompt += f"---INPUT DO USUÁRIO: {user_question}"

    final_prompt = textwrap.dedent(final_prompt)  # Remove indentations for better formatting
    
    return {"final_prompt": final_prompt}
    

    
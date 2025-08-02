import textwrap
from typing import Dict, Any

from src.api.database.models import HistoricoChat, ChatResumes

def prompt_build(state: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Utiliza o histórico do chat carregado e monta o prompt final a ser processado pelo agente de IA.
    '''
    chat_resume: ChatResumes | None  = state.get("chat_resume", None)
    historico_chat: list[HistoricoChat] | None = state.get("chat_history", None)
    user_question = state.get("prompt", None)

    print(state)

    final_prompt = ""

    if chat_resume:
        final_prompt += f"---RESUMO DO HISTÓRICO DO CHAT COM O USUÁRIO--- \n {chat_resume.resume} \n\n"

    if historico_chat:
        final_prompt += f"---HISTÓRICO RECENTE DO CHAT---: \n "
        for historico in [h for h in historico_chat if not h.compacted]:
            final_prompt += f"USUÁRIO: {historico.prompt_description.replace('\n', '').replace('\r', '')} \n"
            final_prompt += f"IA: {historico.response_description.replace('\n', '').replace('\r', '')} \n"
        
        final_prompt += "\n"

    final_prompt += f"---INPUT DO USUÁRIO: {user_question}"

    final_prompt = textwrap.dedent(final_prompt)  # Remove indentations for better formatting
    
    return {"final_prompt": final_prompt}
    

    
from typing import Any, Dict
from langchain_core.memory import BaseMemory

from api.services.dbService import getHistoryChatByThreadID

class CustomSQLChatMemory(BaseMemory):
    def __init__(self, thread_id: str):
        self.thread_id = thread_id

    @property
    def memory_variables(self) -> list[str]:
        return ["chat_history"]

    async def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        '''Buscar o hístorico do chat no banco de dados.'''
        
        result_sql = await getHistoryChatByThreadID(self.thread_id)

        if not result_sql:
            return {"chat_history": "⚠️ Aviso do sistema: O histórico de conversas não pôde ser carregado neste momento. Tente novamente mais tarde."}

        # Construir o histórico no formato esperado pelo LLM
        historico = ""
        for msg in reversed(result_sql):  # manter ordem cronológica
            historico += f"Usuário: {msg.prompt_description}\nIA: {msg.response_description}\n"

        return {"chat_history": historico}

    async def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        # Sem ação necessária, pois a API já está salvando
        return
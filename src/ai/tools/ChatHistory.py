from typing import Any, Dict
from langchain_core.memory import BaseMemory
from sqlalchemy.ext.asyncio import AsyncSession

class CustomSQLChatMemory(BaseMemory):
    def __init__(self, thread_id: str):
        self.thread_id = thread_id

    @property
    def memory_variables(self) -> list[str]:
        return ["chat_history"]

    async def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        '''Buscar o hístorico do chat no banco de dados.'''
        
        result = await self.db.execute(
            select(Mensagem)
            .where(Mensagem.usuario_id == self.user_id)
            .order_by(desc(Mensagem.data))
            .limit(10)
        )
        mensagens = result.scalars().all()

        # Construir o histórico no formato esperado pelo LLM
        historico = ""
        for msg in reversed(mensagens):  # manter ordem cronológica
            historico += f"Usuário: {msg.pergunta}\nIA: {msg.resposta}\n"

        return {"chat_history": historico}

    async def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        # Sem ação necessária, pois a API já está salvando
        return
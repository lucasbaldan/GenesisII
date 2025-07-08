import traceback
import uuid
from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.langgraph.graph import build_graph
from src.api.shared.schemas import ConsultaAgent, ResponseAgent
from src.api.database.engine import get_session_engine
from src.api.database.models import HistoricoChat


router = APIRouter(prefix="/ia", tags=["IA"])

@router.post("/consultar")
async def consultar_agente(consulta: ConsultaAgent,
                           session: AsyncSession = Depends(get_session_engine)):
    """
    Endpoint para consultar o agente IA com uma pergunta.
    Retorna a resposta do agente IA.    
    """
    try:
        graph_chat = build_graph()
        result = await graph_chat.ainvoke({
            "prompt": consulta.prompt,
            "thread_id": consulta.thread_id if consulta.thread_id else "",
            "chat_history": "",
            "resposta_agent": "",
            "final_prompt": ""
        })

        #print(f"Resultado da consulta: \n {result}")
        
        chat_history = HistoricoChat(
            thread_id=consulta.thread_id if consulta.thread_id else str(uuid.uuid4()),
            prompt_description=consulta.prompt,
            response_description=result['resposta_agent'],
            usuario_id=1,
            titulo_chat="Novo Chat" if not consulta.thread_id else None
        )
        session.add(chat_history)
        await session.commit()

        return ResponseAgent(
            resposta_agent = result['resposta_agent'],
            )

    except Exception as e:
        print(f"Erro ao consultar o agente IA: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

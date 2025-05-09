from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai.langgraph import graph

iaAgentControllerRouter = APIRouter(prefix="/ia", tags=["IA"])

class ConsultaAgent(BaseModel):
    prompt: str
    

@iaAgentControllerRouter.post("/consultar")
async def consultar_agente(consulta: ConsultaAgent):
    """
    Endpoint para consultar o agente IA com uma pergunta.
    Retorna a resposta do agente IA.    
    """
    try:
        result = graph.invoke({
            "messages": [
                {"role": "user", "content": consulta.prompt}
            ]
        })

        mensagens = result.get("messages", [])
        ultima_mensagem = None
        for m in reversed(mensagens):
            if hasattr(m, "content"):
                ultima_mensagem = m
                break

        if ultima_mensagem:
            return {"resposta_agent": ultima_mensagem.content}
        else:
            raise HTTPException(status_code=500, detail="O agente não retornou uma resposta válida.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, Request
from pydantic import BaseModel
from ai.langgraph import graph

app = FastAPI()

class Consulta(BaseModel):
    pergunta: str

@app.post("/ia/consultar")
async def consultar_agente(consulta: Consulta):
    try:
        resposta = graph.invoke(consulta.pergunta)
        return {"resposta": resposta}
    except Exception as e:
        return {"erro": str(e)}
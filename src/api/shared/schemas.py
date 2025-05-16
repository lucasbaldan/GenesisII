from pydantic import BaseModel
from datetime import datetime


class ErrorResponse(BaseModel):
    statusCode: int
    message: str
    errors: list[str] | None = None

class ConsultaAgent(BaseModel):
    prompt: str
    
class ResponseAgent(BaseModel):
    resposta_agent: str | None = None

class UsuarioAPI(BaseModel):
    usuario: str
    email: str
    password: str
    nome_completo: str
    cpf: str
    celular1: str
    celular2: str | None = None
    email: str
    password: str

class ResponseUsuario(BaseModel):
    id: int
    usuario: str
    email: str
    nome_completo: str
    cpf: str
    celular1: str
    celular2: str | None = None
    created_at: datetime

class SubJWT(BaseModel):
    user_id: int
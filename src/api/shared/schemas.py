from pydantic import BaseModel
from datetime import datetime

from api.database.models import UserPermissoes


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
    permissoes: list[UserPermissoes] | None = None

class ResponseUsuario(BaseModel):
    id: int
    usuario: str
    email: str
    nome_completo: str
    cpf: str
    celular1: str
    celular2: str | None = None
    created_at: datetime

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AgentMemoryRequest(BaseModel):
    #id: int
    usuario_id: int
    descricao_memoria: str
    faiss_id: str

class HistoricoChatRequest(BaseModel):
    #id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    usuario_id: int
    thread_id: str
    texto_chat: str
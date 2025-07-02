from pydantic import BaseModel
from datetime import datetime

from src.api.database.models import UserPermissoes


class ErrorResponse(BaseModel):
    statusCode: int
    message: str
    errors: list[str] | None = None

class ConsultaAgent(BaseModel):
    prompt: str
    thread_id: str | None = None
    
class ResponseAgent(BaseModel):
    resposta_agent: str | None = None

class UsuarioRequest(BaseModel):
    email: str
    password: str
    nome_completo: str
    cpf: str
    celular1: str
    celular2: str | None = None
    email: str
    password: str
    ativo: bool
    permissoes: list[UserPermissoes] | None = None

class UsuarioListRequest(BaseModel):
    id: int | None = None
    email: str | None = None
    nome_completo: str | None = None
    cpf: str | None = None
    celular1: str | None = None
    celular2: str | None = None
    email: str | None = None
    ativo: bool | None = None

class UsuarioResponse(BaseModel):
    id: int
    email: str
    nome_completo: str
    cpf: str
    celular1: str
    celular2: str | None = None
    created_at: datetime
    ativo: bool

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
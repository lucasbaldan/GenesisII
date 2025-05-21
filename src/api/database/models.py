from datetime import datetime

from enum import Enum

from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, func, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import JSON

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    usuario: Mapped[str] = mapped_column(String(100), unique=True)
    nome_completo: Mapped[str] = mapped_column(String(255))
    cpf: Mapped[str] = mapped_column(String(14), unique=True)
    celular1: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(128))
    celular2: Mapped[str] = mapped_column(String(15), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    permissoes: Mapped[list[int]] = mapped_column(
        JSON, nullable=False, default=lambda: [UserPermissoes.Chat.value]
    )
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    acess_token: Mapped[str] = mapped_column(String(255), init=False, nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), init=False, nullable=True)
    refresh_token_exp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, init=False)

class UserPermissoes(Enum):
    Chat = 1
    Ensinar = 2
    SubmeterArquivos = 3
    GerenciarMemoria = 4
    GerenciarUsuarios = 5

@table_registry.mapped_as_dataclass
class AgentMemory:
    __tablename__ = "agent_memory"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="RESTRICT"))
    descricao_memoria: Mapped[str] = mapped_column(Text)
    faiss_id: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class Agent:
    __tablename__ = "historico_chat"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="RESTRICT"))
    thread_id: Mapped[str] = mapped_column(String(255))
    texto_chat: Mapped[str] = mapped_column(Text)
    origem: Mapped[str] = mapped_column(String(50), comment="Usuário ou IA")
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
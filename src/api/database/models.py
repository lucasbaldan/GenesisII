from datetime import datetime
from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import String, func

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    usuario: Mapped[str] = mapped_column(String(100), unique=True)
    nome_completo: Mapped[str] = mapped_column(String(255))
    cpf: Mapped[str] = mapped_column(String(14), unique=True)
    celular1: Mapped[str] = mapped_column(String(15))
    celular2: Mapped[str] = mapped_column(String(15), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

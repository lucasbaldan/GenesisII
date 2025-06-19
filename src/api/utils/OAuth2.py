from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.api.database.models import User
from src.api.utils.JWT import decode_jwt_token
from src.api.database.engine import get_session_engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/token")

async def get_current_user(
        session: AsyncSession = Depends(get_session_engine),
        token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current user from the JWT token.
    """

    try:
        usuario_id_logado = decode_jwt_token(token)
        if not usuario_id_logado:
            raise Exception("Erro ao decodificar o token")
    
        usuario = await session.execute(
        select(User).where(
            (User.id == usuario_id_logado) & (User.ativo == True) & (User.acess_token == token)
            )
        )
        usuario = usuario.scalar_one_or_none()
        
        if not usuario:
            raise Exception("Usuário não encontrado ativamente na plataforma.")
        
        return usuario
    
    except Exception as e:
        raise Exception("Erro ao decodificar o token -> " + str(e))


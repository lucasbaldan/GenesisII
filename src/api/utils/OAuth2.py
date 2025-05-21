from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from requests import Session
from sqlalchemy import select

from api.database.models import User
from api.utils.JWT import decode_jwt_token
from api.database.engine import get_session_engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/token")

def get_current_user(
        session: Session = Depends(get_session_engine),
        token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current user from the JWT token.
    """

    try:
        usuario_id_logado = decode_jwt_token(token)
        if not usuario_id_logado:
            raise Exception("Erro ao decodificar o token")
    
        usuario: User = session.scalar(
        select(User).where(
            (User.id == usuario_id_logado) & (User.ativo == True) & (User.acess_token == token)
            )
        )

        if not usuario:
            raise Exception("Usuário não encontrado ativamente na plataforma.")
        
        return usuario
    
    except Exception as e:
        raise Exception("Erro ao decodificar o token -> " + str(e))


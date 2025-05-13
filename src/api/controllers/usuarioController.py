from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from requests import Session
from sqlalchemy import select
from api.shared.schemas import UsuarioAPI, ResponseUsuario
from api.database.models import User
from api.database.engine import get_session_engine

usuarioController = APIRouter(prefix="/usuarios", tags=["usuarios"])

@usuarioController.post("/", status_code=HTTPStatus.CREATED, response_model=ResponseUsuario)
async def salvar(usuario: UsuarioAPI, session : Session = Depends(get_session_engine)):
    try:    
              
            verifica_usuario = session.scalar(
                select(User).where(
                    (User.usuario == usuario.usuario) | (User.email == usuario.email) | (User.cpf == usuario.cpf)
                )
            )

            if verifica_usuario:
                if verifica_usuario.email == usuario.email:
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email já cadastrado na plataforma.")
                elif verifica_usuario.cpf == usuario.cpf:
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="CPF já cadastrado na plataforma.")
                else:
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Usuário já cadastrado na plataforma.")


            novo_usuario = User(
                usuario=usuario.usuario,
                email=usuario.email,
                password=usuario.password,
                nome_completo=usuario.nome_completo,
                cpf=usuario.cpf,
                celular1=usuario.celular1,
                celular2=usuario.celular2
            )

            session.add(novo_usuario)
            session.commit()
            session.refresh(novo_usuario)

            return novo_usuario

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

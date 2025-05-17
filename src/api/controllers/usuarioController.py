from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session
from sqlalchemy import select
from api.shared.schemas import SubJWT, UsuarioAPI, ResponseUsuario
from api.database.models import User
from api.database.engine import get_session_engine
from api.utils.PasswordHash import hash_password, verify_password
from api.utils.JWT import create_jwt_token
from api.utils.OAuth2 import get_current_user

usuarioController = APIRouter(prefix="/usuarios", tags=["usuarios"])

@usuarioController.post("/", status_code=HTTPStatus.CREATED, response_model=ResponseUsuario)
async def salvar(usuario: UsuarioAPI, 
                 session : Session = Depends(get_session_engine),
                 ):
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
                password=hash_password(usuario.password),
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
    

@usuarioController.put("/{id}", status_code=HTTPStatus.OK, response_model=ResponseUsuario)
async def atualizar_usuario(
    id: int,
    usuario: UsuarioAPI,
    session: Session = Depends(get_session_engine)
):
    try:

        usuario_db = session.scalar(
            select(User).where(User.id == id).limit(1)
            )
        if not usuario_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado na base de dados.")
        
        usuario_db.usuario = usuario.usuario
        usuario_db.email = usuario.email
        usuario_db.nome_completo = usuario.nome_completo
        usuario_db.cpf = usuario.cpf
        usuario_db.celular1 = usuario.celular1
        usuario_db.celular2 = usuario.celular2

        if usuario.password:
            usuario_db.password = hash_password(usuario.password)

        session.commit()
        session.refresh(usuario_db)

        return usuario_db

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@usuarioController.get("/", status_code=HTTPStatus.OK, response_model=list[ResponseUsuario])
async def listar(
    limit: int = 100,
    page: int = 1,
    session: Session = Depends(get_session_engine),
    current_user=Depends(get_current_user)
    ):
    try:
        usuarios = session.scalars(
           select(User).limit(limit).offset((page - 1) * limit)
        ).all()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@usuarioController.get("/{id}", status_code=HTTPStatus.OK, response_model=ResponseUsuario)
async def buscar_usuario(
    id: int,
    session: Session = Depends(get_session_engine)
):
    try:
        usuario = session.scalar(
            select(User).where(User.id == id).limit(1)
            )
        if not usuario:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@usuarioController.delete("/{id}", status_code=HTTPStatus.OK)
async def deletar_usuario(
    id: int,
    session: Session = Depends(get_session_engine)
):
    try:
        usuario = session.scalar(
            select(User).where(User.id == id).limit(1)
            )
        if not usuario:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
        
        session.delete(usuario)
        session.commit()
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@usuarioController.post("/token", status_code=HTTPStatus.OK)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session_engine)
):
    try:
        verifica_usuario: User = session.scalar(
            select(User).where(
                (User.cpf == data.username) | (User.email == data.username)
                ).limit(1)
            )
        if not verifica_usuario or not verify_password(data.password, verifica_usuario.password):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário ou senha inválidos para acesso a aplicação.")
        
        
        acess_token = create_jwt_token(data=verifica_usuario.id)
        return acess_token
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@usuarioController.post("/me", status_code=HTTPStatus.OK)
async def login(
    current_user=Depends(get_current_user)
):
    return current_user
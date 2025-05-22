from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from sqlalchemy import select

from api.shared.Annotateds import T_Current_User, T_Session, T_OAuth2_Request_Form
from api.shared.schemas import  RefreshTokenRequest, UsuarioAPI, ResponseUsuario
from api.database.models import User
from api.utils.PasswordHash import hash_password, verify_password
from api.utils.JWT import create_jwt_token

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ResponseUsuario)
async def salvar(usuario: UsuarioAPI, 
                 session: T_Session
                 ):
    try:    
              
            verifica_usuario = session.scalar(
                select(User).where(
                    (User.email == usuario.email) | (User.cpf == usuario.cpf)
                )
            )

            if verifica_usuario:
                if verifica_usuario.email == usuario.email:
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email já cadastrado na plataforma.")
                else:
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="CPF já cadastrado na plataforma.")


            novo_usuario = User(
                email=usuario.email,
                password=hash_password(usuario.password),
                nome_completo=usuario.nome_completo,
                cpf=usuario.cpf,
                celular1=usuario.celular1,
                celular2=usuario.celular2,
                permissoes=[p.value for p in usuario.permissoes],
                ativo=usuario.ativo,
            )

            session.add(novo_usuario)
            session.commit()
            session.refresh(novo_usuario)

            return novo_usuario
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/{id}", status_code=HTTPStatus.OK, response_model=ResponseUsuario)
async def atualizar_usuario(
    id: int,
    usuario: UsuarioAPI,
    session: T_Session
):
    try:

        usuario_db = session.scalar(
            select(User).where(User.id == id).limit(1)
            )
        if not usuario_db:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado na base de dados.")
        
        usuario_db.email = usuario.email
        usuario_db.nome_completo = usuario.nome_completo
        usuario_db.cpf = usuario.cpf
        usuario_db.celular1 = usuario.celular1
        usuario_db.celular2 = usuario.celular2
        usuario_db.permissoes = [p.value for p in usuario.permissoes]
        usuario_db.ativo = usuario.ativo


        if usuario.password:
            usuario_db.password = hash_password(usuario.password)

        session.commit()
        session.refresh(usuario_db)

        return usuario_db

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/", status_code=HTTPStatus.OK, response_model=list[ResponseUsuario])
async def listar(
    current_user: T_Current_User,
    session: T_Session,
    limit: int = 100,
    page: int = 1,
    ):
    try:
        usuarios = session.scalars(
           select(User).limit(limit).offset((page - 1) * limit)
        ).all()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", status_code=HTTPStatus.OK, response_model=ResponseUsuario)
async def buscar_usuario(
    id: int,
    session: T_Session
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
    

@router.delete("/{id}", status_code=HTTPStatus.OK)
async def deletar_usuario(
    id: int,
    session: T_Session
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
    
@router.post("/token", status_code=HTTPStatus.OK)
async def login(
    session: T_Session,
    data: T_OAuth2_Request_Form
 ):
    try:
        verifica_usuario: User = session.scalar(
            select(User).where(
                ((User.cpf == data.username) | (User.email == data.username)) & (User.ativo == True)
                ).limit(1)
            )
        if not verifica_usuario or not verify_password(data.password, verifica_usuario.password):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário ou senha inválidos para acesso a aplicação.")
        
        
        acess_token = create_jwt_token(data=verifica_usuario.id)

        verifica_usuario.acess_token = acess_token["access_token"]
        verifica_usuario.refresh_token = acess_token["refresh_token"]
        verifica_usuario.refresh_token_exp = acess_token["expires(datetime)"]
        session.commit()

        return acess_token
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/refreshToken", status_code=HTTPStatus.OK)
async def login(
    session: T_Session,
    current_user: T_Current_User,
    dados: RefreshTokenRequest
 ):
    try: 
        exp = current_user.refresh_token_exp
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)

        if current_user.refresh_token != dados.refresh_token or exp < datetime.now(tz=timezone.utc):
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Ocorreu um erro ao renovar autenticação na api.")
        
        acess_token = create_jwt_token(data=current_user.id)

        current_user.acess_token = acess_token["access_token"]
        current_user.refresh_token = acess_token["refresh_token"]
        current_user.refresh_token_exp = acess_token["expires(utc)"]
        session.commit()

        return acess_token
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
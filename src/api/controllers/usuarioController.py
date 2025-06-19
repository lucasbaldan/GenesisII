from datetime import datetime, timezone

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.engine import get_session_engine
from src.api.shared.Annotateds import T_Current_User, T_OAuth2_Request_Form
from src.api.shared.schemas import  RefreshTokenRequest, UsuarioRequest, UsuarioResponse, UsuarioListRequest
from src.api.database.models import User
from src.api.utils.PasswordHash import hash_password, verify_password
from src.api.utils.JWT import create_jwt_token

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=UsuarioResponse)
async def salvar(
    current_user: T_Current_User,
    usuario: UsuarioRequest, 
    session: AsyncSession = Depends(get_session_engine),
                 ):
    try:       
            result_check_usuario = await session.execute(
                select(User).where(
                    (User.email == usuario.email) | (User.cpf == usuario.cpf)
                )
            )
            verifica_usuario = result_check_usuario.scalar_one_or_none()

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
            await session.commit()
            await session.refresh(novo_usuario)

            return novo_usuario
    
    except HTTPException as e:
        raise e
    

@router.put("/{id}", status_code=HTTPStatus.OK, response_model=UsuarioResponse)
async def atualizar_usuario(
    current_user: T_Current_User,
    id: int,
    usuario: UsuarioRequest,
    session: AsyncSession = Depends(get_session_engine)
):
    try:
        verifica_usuario_db = await session.execute(
            select(User).where(User.id == id).limit(1)
            )
        usuario_db = verifica_usuario_db.scalar_one_or_none()
        
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

        await session.commit()
        await session.refresh(usuario_db)

        return usuario_db

    except HTTPException as e:
        raise e
    

@router.post("/list", status_code=HTTPStatus.OK, response_model=list[UsuarioResponse])
async def listar(
    filtro: UsuarioListRequest,
    #current_user: T_Current_User,
    session: AsyncSession = Depends(get_session_engine),
    limit: int = 100,
    page: int = 1,
    ):

    try:
        query = select(User).limit(limit).offset((page - 1) * limit)

        if filtro.id:
            query = query.where(User.id.contains(filtro.id))
        if filtro.nome_completo:
            query = query.where(User.nome_completo.contains(filtro.nome_completo))
        if filtro.cpf:
            query = query.where(User.cpf.contains(filtro.cpf))
        if filtro.email:
            query = query.where(User.email.contains(filtro.email))
        if filtro.celular1:
            query = query.where(User.celular1.contains(filtro.celular1))
        if filtro.celular2:
            query = query.where(User.celular2.contains(filtro.celular2))
        if filtro.ativo:
            query = query.where(User.ativo == filtro.ativo)

        usuarios = await session.execute(query)
        usuarios = usuarios.scalars().all()
           
        return usuarios
    
    except HTTPException:
        raise


@router.get("/{id}", status_code=HTTPStatus.OK, response_model=UsuarioResponse)
async def buscar_usuario(
    current_user: T_Current_User,
    id: int,
    session: AsyncSession = Depends(get_session_engine)
):
    try:
        verifica_usuario = await session.execute(
            select(User).where(User.id == id).limit(1)
            )
        usuario = verifica_usuario.scalar_one_or_none()

        if not usuario:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
        return usuario
    
    except HTTPException as e:
        raise e
    

@router.delete("/{id}", status_code=HTTPStatus.OK)
async def deletar_usuario(
    current_user: T_Current_User,
    id: int,
    session: AsyncSession = Depends(get_session_engine)
):
    try:
        verifica_usuario = await session.execute(
            select(User).where(User.id == id).limit(1)
            )
        usuario = verifica_usuario.scalar_one_or_none()

        if not usuario:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
        
        session.delete(usuario)
        await session.commit()
        
        return
    except HTTPException as e:
        raise e
    
@router.post("/token", status_code=HTTPStatus.OK)
async def login(
    data: T_OAuth2_Request_Form,
    session: AsyncSession = Depends(get_session_engine)
 ):
    try:
        verifica_usuario = await session.execute(
            select(User).where(
                ((User.cpf == data.username) | (User.email == data.username)) & (User.ativo == True)
                ).limit(1)
            )
        verifica_usuario = verifica_usuario.scalar_one_or_none()

        if not verifica_usuario or not verify_password(data.password, verifica_usuario.password):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário ou senha inválidos para acesso a aplicação.")
        
        
        acess_token = create_jwt_token(data=verifica_usuario.id)

        verifica_usuario.acess_token = acess_token["access_token"]
        verifica_usuario.refresh_token = acess_token["refresh_token"]
        verifica_usuario.refresh_token_exp = acess_token["expires(datetime)"]
        await session.commit()

        return acess_token
    
    except HTTPException as e:
        raise e
    
@router.post("/refreshToken", status_code=HTTPStatus.OK)
async def login(
    current_user: T_Current_User,
    dados: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session_engine),
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
        await session.commit()

        return acess_token
    
    except HTTPException as e:
        raise e
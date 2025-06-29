from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.auth import autenticar, criar_token_acesso
from core.deps import get_current_user, get_session
from core.security import gerar_hash_senha
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import (UsarioSchemaUp, UsuarioSchemaArtigos,
                                    UsuarioSchemaBase, UsuarioSchemaCreate)

router = APIRouter()

NOT_FOUND = "Usuário não encontrado!"
EMAIL_ALREAD_EXIST = "O email informado ja foi utilizado!"

"""_summary_
Usuário logado
"""
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario: UsuarioModel = Depends(get_current_user)):
    return usuario

"""_summary_
Criar usuário
"""
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(nome=usuario.nome, sobrenome=usuario.sobrenome,
                                              email=usuario.email, senha=gerar_hash_senha(usuario.senha),
                                              eh_admin=usuario.eh_admin)
    async with db as session:
        try:
           session.add(novo_usuario)
           await session.commit()
           return novo_usuario
        except IntegrityError:
            raise HTTPException(detail=EMAIL_ALREAD_EXIST, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    

"""_summary_
Login
"""
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)): 
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    
    if not usuario:
        raise HTTPException(detail=NOT_FOUND,status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"},
                        status_code=status.HTTP_200_OK)

    

"""_summary_
Lista de  usuários
"""
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)): 
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        
        return usuarios
    

"""_summary_
Obtem Usuário logado
"""
@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario = UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        
        if usuario:
            return usuario
        else:
            raise HTTPException(detail=NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)    
        
"""_summary_
Atualiza um usuario
Raises:
    HTTPException: _description_

Returns:
    _type_: _description_
"""
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def get_usuario(usuario_id: int, usuario: UsarioSchemaUp,  db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        
        if usuario_up: 
            await mapper(usuario, usuario_up)
            await session.commit(); 
            return usuario_up
        else:
            raise HTTPException(detail=NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)    
 


"""_summary_
Deleta um Usuário
"""
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario = UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        
        if usuario:
            await session.delete(usuario)
            await session.commit()
        else:
            raise HTTPException(detail=NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)  
       

async def mapper( usuario_inbound: UsarioSchemaUp, usuario_up: UsuarioSchemaBase) -> UsuarioSchemaBase:
    print('Mapeando ...')
    if usuario_inbound.nome:
        usuario_up.nome = usuario_inbound.nome
    if usuario_inbound.sobrenome:
        usuario_up.sobrenome = usuario_inbound.sobrenome
    if usuario_inbound.email:
        usuario_up.email = usuario_inbound.email
    if usuario_inbound.eh_admin:
        usuario_up.eh_admin = usuario_inbound.eh_admin
    if usuario_inbound.senha:
        usuario_up.senha = gerar_hash_senha(usuario_inbound.senha)
    return usuario_inbound    
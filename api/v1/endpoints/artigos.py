from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_current_user, get_session
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema

router = APIRouter()

NOT_FOUND = "Recurso não encontrado!"
ACTION_DENIED = "Você não tem permissão para esta ação!"

"""_summary_
Cria um artigo
"""
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario: UsuarioModel = Depends(get_current_user), 
                      db: AsyncSession = Depends(get_session)):
    novo_artigo = ArtigoModel(
        titulo=artigo.titulo, 
        descricao=artigo.descricao,
        url_fonte=artigo.url_fonte,
        usuario_id=usuario.id
        )
    
    db.add(novo_artigo)
    await db.commit()
    return novo_artigo


"""_summary_
Lista de artigos
Returns:
    _type_: _description_
"""
@router.get('/', response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()
        
        return artigos 


"""_summary_
Obtem artigo
Returns:
    _type_: _description_
"""
@router.get('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo:
            return artigo
        else:
            raise HTTPException(detail=NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        


"""_summary_
Atualiza um artigos
Returns:
    _type_: _description_
"""
@router.put('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def get_artigos(artigo_up: ArtigoSchema, artigo_id: int, db: AsyncSession = Depends(get_session), usuario: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo:
            await mapper(artigo_up, artigo, usuario.id) 
            await session.commit()
            return artigo
        else:
            raise HTTPException(detail=NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        

"""_summary_
Deleta um artigo
Returns:
    _type_: _description_
"""
@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def get_artigo(artigo_id: int, 
                     db: AsyncSession = Depends(get_session), 
                     usuario: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()
        
        if artigo:
            
            if artigo.usuario_id == usuario.id:
                session.delete(artigo)
                await session.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                raise HTTPException(detail=ACTION_DENIED, status_code=status.HTTP_401_UNAUTHORIZED)
                
        else:
            raise HTTPException(detail=NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        


async def mapper(artigo_inbound: ArtigoSchema, artigo_model: ArtigoModel, id_usuario_logado: int) -> ArtigoModel:
    print('Mapeando ...', id_usuario_logado, artigo_model.usuario_id, " São diferentes ?", id_usuario_logado != artigo_model.usuario_id)
    if artigo_inbound.titulo:
        artigo_model.titulo = artigo_inbound.titulo
    if artigo_inbound.descricao:
        artigo_model.descricao = artigo_inbound.descricao
    if artigo_inbound.url_fonte:
        artigo_model.url_fonte = artigo_inbound.url_fonte 
    if artigo_model.usuario_id != id_usuario_logado:
        artigo_model.usuario_id = id_usuario_logado
    return artigo_model
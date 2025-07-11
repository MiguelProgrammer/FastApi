from datetime import datetime, timedelta
from typing import List, Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import EmailStr
from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.configs import settings
from core.security import verificar_senha
from models.usuario_model import UsuarioModel

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> (UsuarioModel | None):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()
        
        if not usuario:
            return None
        if not verificar_senha(senha, usuario.senha):
            return None
        
        return usuario

def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    """_summary_
    https://datatracker.ietf.org/doc/html/rfc7519#ssection-4.1.3
    Args:
        tipo_token (str): _description_
        tempo_vida (timedelta): _description_
        sub (str): _description_

    Returns:
        str: _description_
    """
    payload = {}
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida
    
    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    """_summary_
    https://jwt.io
    Args:
        sub (str): _description_

    Returns:
        str: _description_
    """
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
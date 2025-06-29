from typing import ClassVar, List

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:postgresql@localhost:5432/faculdade'
    DBBaseModel: ClassVar[type[DeclarativeBase]] = declarative_base()
    
    JWT_SECRET: str = 'UsJyqraXWKUSNbFPDa5HrJhzP4umpxMZO54Wzq6pKmk'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True
        
settings: Settings = Settings()
from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

"""_summary_
    Verifica se a senha está correta
"""
def verificar_senha(senha: str, hash_senha: str) -> bool:
    return CRIPTO.verify(senha, hash_senha)

"""_summary_
Gera hash senha
"""
def gerar_hash_senha(senha: str) -> str:
    return CRIPTO.hash(senha)
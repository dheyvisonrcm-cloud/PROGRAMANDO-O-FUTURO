
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Defina a variável SECRET_KEY no arquivo .env")

ALGORITMO = "HS256"
EXPIRA_MINUTOS = 60 * 24  # o token vale 24 horas


def gerar_hash(senha: str) -> str:
    # bcrypt só considera os primeiros 72 bytes da senha
    return bcrypt.hashpw(senha.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode("utf-8")[:72], senha_hash.encode("utf-8"))
    except ValueError:
        return False


def criar_token(id_usuario: int) -> str:
    payload = {
        "sub": str(id_usuario),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRA_MINUTOS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITMO)


def ler_token(token: str):
    """Devolve o id do usuário, ou None se o token for inválido ou estiver expirado."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None